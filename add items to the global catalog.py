# global catalog
global_catalog = [
    {'title': 'Book A', 'author': 'Author A', 'isbn': '1234567890'},
    {'title': 'Book B', 'author': 'Author B', 'isbn': '0987654321'}
    # ... other books/items
]

# add an item to the catalog
def add_item_to_catalog(catalog, title, author, isbn):
    """
    Add a new item to the global catalog.

    :param catalog: List of dictionaries representing the catalog.
    :param title: Title of the book/item.
    :param author: Author of the book/item.
    :param isbn: ISBN of the book/item.
    """
    new_item = {
        'title': title,
        'author': author,
        'isbn': isbn
    }
    catalog.append(new_item)
    print(f"'{title}' by {author} has been added to the catalog.")

# Example usage
add_item_to_catalog(global_catalog, 'New Book', 'New Author', '1112223334445')
