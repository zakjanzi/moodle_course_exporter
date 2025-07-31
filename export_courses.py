import re

def escape_quotes(text):
    return text.replace("'", "''")

def generate_sql(course_tuples):
    sql_parts = []
    for i, (course, pattern) in enumerate(course_tuples):
        course_safe = escape_quotes(course)
        sql = f"""SELECT
  CONCAT(
    COALESCE((
      SELECT id FROM mdl_course
      WHERE LOWER(fullname) LIKE '{pattern}'
      LIMIT 1
    ), 'N/A'),
    ',', '{course_safe}'
  )"""
        sql_parts.append(sql)
    return " UNION ALL\n".join(sql_parts)


def format_course_name(name):
    """Extract main keywords from the course title for a fuzzy LIKE match."""
    # Remove leading numbers, punctuation, stopwords etc.
    name = re.sub(r"^[0-9]+[\.\)]*\s*", "", name.lower())
    keywords = re.findall(r'\b[a-z]+\b', name)
    if not keywords:
        return "%%"
    pattern = "%" + "%".join(keywords) + "%"
    return pattern

def main():
    print("Paste your course list (one per line), then enter an empty line:")
    lines = []
    while True:
        try:
            line = input()
        except EOFError:
            break
        if line.strip() == "":
            break
        lines.append(line.strip())

    course_tuples = [(line, format_course_name(line)) for line in lines]
    sql_query = generate_sql(course_tuples)

    # Write SQL query to a file
    with open("courselist_query.sql", "w") as f:
        f.write(sql_query)

    final_command = '''sudo mysql -u root -p middledb --batch --raw --skip-column-names -e "$(cat courselist_query.sql)" > ~/courselist/mathgr_output.csv'''

    print("\nGenerated SQL written to courselist_query.sql\n")
    print("Run the following command on your server:\n")
    print(final_command)

if __name__ == "__main__":
    main()
