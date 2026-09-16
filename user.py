from admin import (
    load_library,
    save_library,
    find_book
)


def books_in_category(books, category):
    category = category.strip().lower()

    result = []

    for book_id, book in books.items():
        if book["category"].strip().lower() == category:
            result.append(book_id)

    return result


def search_by_title(books, search_text):
    search_text = search_text.strip().lower()

    result = []

    for book_id, book in books.items():
        if search_text in book["title"].lower():
            result.append(book_id)

    return result


def borrow_book(
    books,
    loans,
    search_text,
    borrower
):
    if not borrower.strip():
        return "EMPTY_NAME"

    book_id = find_book(books, search_text)

    if book_id is None:
        return "BOOK_NOT_FOUND"

    if not books[book_id]["available"]:
        return "NOT_AVAILABLE"

    books[book_id]["available"] = False

    loans.append(
        {
            "book_id": book_id,
            "borrower": borrower
        }
    )

    return "OK"


def return_book(
    books,
    loans,
    book_title,
    borrower
):
    if not borrower.strip():
        return "EMPTY_NAME"

    book_id = find_book(books, book_title)

    if book_id is None:
        return "BOOK_NOT_FOUND"

    if books[book_id]["available"]:
        return "NOT_ON_LOAN"

    matching_loan = None

    for loan in loans:
        if (
            loan["book_id"] == book_id
            and loan["borrower"].strip().lower()
            == borrower.strip().lower()
        ):
            matching_loan = loan
            break

    if matching_loan is None:
        return "NOT_ON_LOAN"

    loans.remove(matching_loan)

    books[book_id]["available"] = True

    return "OK"


def main():
    data = load_library("library.json")

    books = data["books"]
    loans = data["loans"]

    while True:
        print("\nLIBRARY USER SYSTEM")
        print("=" * 60)
        print("1. Search books by title")
        print("2. Search books by category")
        print("3. Borrow a book")
        print("4. Return a book")
        print("5. Exit")

        choice = input("Select an option: ").strip()

        if choice == "1":
            search_text = input("Enter title: ")

            results = search_by_title(
                books,
                search_text
            )

            if results:
                for book_id in results:
                    book = books[book_id]

                    if book["available"]:
                        status = "AVAILABLE"
                    else:
                        status = "ON LOAN"

                    print(
                        f"{book_id} | "
                        f"{book['title']} | "
                        f"{book['author']} | "
                        f"{status}"
                    )
            else:
                print("No books found.")

        elif choice == "2":
            category = input("Enter category: ")

            results = books_in_category(
                books,
                category
            )

            if results:
                for book_id in results:
                    book = books[book_id]

                    if book["available"]:
                        status = "AVAILABLE"
                    else:
                        status = "ON LOAN"

                    print(
                        f"{book_id} | "
                        f"{book['title']} | "
                        f"{status}"
                    )
            else:
                print("No books found.")

        elif choice == "3":
            search_text = input(
                "Enter book ID, title, or author: "
            )

            borrower = input(
                "Enter borrower name: "
            )

            result = borrow_book(
                books,
                loans,
                search_text,
                borrower
            )

            print(result)

        elif choice == "4":
            search_text = input(
                "Enter book ID or title: "
            )

            borrower = input(
                "Enter borrower name: "
            )

            result = return_book(
                books,
                loans,
                search_text,
                borrower
            )

            print(result)

        elif choice == "5":
            save_library(
                data,
                "library.json"
            )

            print("Library data saved.")
            print("Goodbye!")
            break

        else:
            print("Invalid selection.")


if __name__ == "__main__":
    main()