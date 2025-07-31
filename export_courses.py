def generate_sql(course_tuples):
    sql_parts = []
    for i, (course, pattern) in enumerate(course_tuples):
        sql = f'''SELECT
  COALESCE((
    SELECT id FROM mdl_course
    WHERE LOWER(fullname) LIKE '{pattern}'
    LIMIT 1
  ), 'N/A') AS id{i+1},
  '{course}'
'''
        sql_parts.append(sql)
    full_sql = " UNION ALL\n".join(sql_parts)
    return full_sql

def format_course_name(name):
    # Clean and add % for LIKE pattern
    clean_name = name.strip().lower()
    return f"%{clean_name}%"

def main():
    print("Paste your course list (one per line), then enter an empty line:")
    lines = []
    while True:
        line = input()
        if line.strip() == "":
            break
        lines.append(line.strip())

    course_tuples = [(line, format_course_name(line)) for line in lines]
    sql_query = generate_sql(course_tuples)

    final_command = f'''sudo mysql -u root -p middledb --batch --raw --skip-column-names -e "
{sql_query}
" > ~/courselist/mathgr_output.csv'''

    print("\nGenerated command:\n")
    print(final_command)

if __name__ == "__main__":
    main()
