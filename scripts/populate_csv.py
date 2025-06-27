import psycopg as psy
from psycopg.rows import dict_row
from collections import defaultdict


if __name__ == '__main__':
    conn = psy.connect('dbname=pt-stackoverflow user=postgres', row_factory=dict_row)
    cur = conn.cursor(name='cur')
    question_cur = conn.cursor(name='question_cur')

    #Query for all tags
    tags = cur.execute("""
                        SELECT DISTINCT tag_name
                        FROM tags
                        """).fetchall()

    BATCH_SIZE = 10000
    query = question_cur.execute("""
                                SELECT id, tags, owner_user_id FROM posts
                                WHERE post_type_id = 1
                                 """)
    
    ans = defaultdict(lambda: defaultdict(int))
    counts = defaultdict(int)

    while True:
        data = query.fetchmany(BATCH_SIZE)
        if not data: break

        #Build qid -> tags dict
        to_tag = {p['id']: p['tags'] for p in data}

        #Get all answers
        answers = cur.execute("""
                              SELECT parent_id, owner_user_id FROM posts
                              WHERE parent_id = ANY(%s) and post_type_id = 2
                              """, (list(to_tag.keys()),)).fetchall()

        #Index
        for p in data:
            for t in p['tags']: 
                ans[p['owner_user_id']][t] += 1
                counts[t] += 1
        for a in answers:
            tags = to_tag[a['parent_id']]
            for t in tags: 
                counts[t] += 1
                ans[a['owner_user_id']][t] += 1
    
    #Minimum amount of posts
    MIN_POSTS = 2000
    filtered_tags = [t for t,c in counts.items() if c > MIN_POSTS]
    print(f"Filtered to {len(filtered_tags)} tags")

    #Get associated user data
    users = cur.execute("""
                        SELECT id, reputation, views, up_votes, down_votes FROM users
                        WHERE id = ANY(%s)
                        """, (list(ans.keys()),)).fetchall()

    user_meta = list(users[0].keys())
    #Work on output
    with open('output.csv', 'w') as outp:
        #Header
        outp.write(f"{','.join(user_meta)},count_tags,{','.join(filtered_tags)}\n")
        #data rows
        for u in users:
            tag_freq = ans[u['id']]
            outp.write(f"{','.join([str(u[k]) for k in user_meta])},{len(tag_freq)},{','.join([str(tag_freq.get(t,0)) for t in filtered_tags])}\n")