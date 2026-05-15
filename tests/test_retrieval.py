from rag.retrieve import retrieve_assessments

queries = [
    "Java developer",
    "Leadership role",
    "Sales manager",
    "Personality assessment",
    "Cognitive ability"
]

for query in queries:

    print("\n" + "=" * 50)
    print("QUERY:", query)
    print("=" * 50)

    results = retrieve_assessments(query)

    for i, item in enumerate(results, 1):

        print(f"\n{i}. {item['name']}")
        print(item['url'])