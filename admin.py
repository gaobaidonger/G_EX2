import json


def load_library(filename):
    with open(filename, "r", encoding="utf-8") as file:
        return json.load(file)


def save_library(data, filename):
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


def find_book(books, search_text):
    search_text = str(search_text).strip().lower()

    for book_id, book in books.items():
        if book_id.lower() == search_text:
            return book_id

        if book["title"].strip().lower() == search_text:
            return book_id

        if book["author"].strip().lower() == search_text:
            return book_id

    return None


def display_books(books):
    print("\nBOOK CATALOGUE")
    print("-" * 60)

    for book_id, book in books.items():
        if book["available"]:
            status = "AVAILABLE"
        else:
            status = "ON LOAN"

        print(
            f"{book_id} | "
            f"{book['title']} | "
            f"{book['category']} | "
            f"{status}"
        )


def display_loans(loans, books):
    print("\nCURRENT LOANS")
    print("-" * 60)

    for loan in loans:
        book_id = loan["book_id"]

        if book_id in books:
            title = books[book_id]["title"]

            print(
                f"{book_id} | "
                f"{title} | "
                f"Borrower: {loan['borrower']}"
            )


def library_statistics(books):
    total = len(books)

    available = 0

    for book in books.values():
        if book["available"]:
            available += 1

    borrowed = total - available

    return total, available, borrowed


def main():
    data = load_library("library.json")

    library = data["library"]
    categories = data["categories"]
    books = data["books"]
    loans = data["loans"]

    print("LIBRARY ADMINISTRATION")
    print("=" * 60)

    print(f"Library: {library['name']}")
    print(f"Branch: {library['branch']}")
    print(f"Year: {library['year']}")
    print(f"Categories: {', '.join(categories)}")

    display_books(books)

    display_loans(loans, books)

    total, available, borrowed = library_statistics(books)

    print("\nSTATISTICS")
    print("-" * 60)
    print(f"Total books: {total}")
    print(f"Available: {available}")
    print(f"Borrowed: {borrowed}")


if __name__ == "__main__":
    main()