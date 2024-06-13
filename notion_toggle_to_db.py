from notion_client import Client

# Initialize the client
notion = Client(auth="your_notion_token")

# Replace with your page and database IDs
PAGE_ID = "your_page_id"
DATABASE_ID = "your_database_id"

# Define the static tag
STATIC_TAG = "Your Static Tag Text"

def get_toggle_details(block_id):
    block = notion.blocks.retrieve(block_id)
    if block["type"] == "toggle":
        title = "Untitled"
        if block["toggle"].get("rich_text") and len(block["toggle"]["rich_text"]) > 0:
            title = block["toggle"]["rich_text"][0].get("plain_text", "Untitled")
        
        # Debug: Print the block details
        print(f"Block ID: {block_id}, Title: {title}")

        children = notion.blocks.children.list(block_id)["results"]
        
        # Debug: Print the children details
        print(f"Children of Block {block_id}: {children}")

        content = " ".join(
            child["paragraph"]["rich_text"][0]["plain_text"]
            if child["type"] == "paragraph" and child["paragraph"].get("rich_text") and len(child["paragraph"]["rich_text"]) > 0
            else ""
            for child in children
        )
        
        # Debug: Print the content extracted
        print(f"Content of Block {block_id}: {content}")

        return title, content
    return None, None

def add_to_database(title, content):
    response = notion.pages.create(
        parent={"database_id": DATABASE_ID},
        properties={
            "Title": {
                "title": [
                    {
                        "text": {
                            "content": title
                        }
                    }
                ]
            },
            "Content": {
                "rich_text": [
                    {
                        "text": {
                            "content": content
                        }
                    }
                ]
            },
            "Tags": {
                "multi_select": [
                    {
                        "name": STATIC_TAG
                    }
                ]
            }
        }
    )
    print(f"Added to database: {title}, Content: {content}, Tag: {STATIC_TAG}")

# Retrieve the blocks on the page
blocks = notion.blocks.children.list(PAGE_ID)["results"]

print(f"Found {len(blocks)} blocks on the page.")

for block in blocks:
    if block["type"] == "toggle":
        print(f"Processing toggle block: {block['id']}")
        title, content = get_toggle_details(block["id"])
        if title and content:
            print(f"Title: {title}, Content: {content}")
            add_to_database(title, content)
        else:
            print(f"Skipped block: {block['id']} due to missing title or content.")

print("Completed transferring toggle lists to database.")