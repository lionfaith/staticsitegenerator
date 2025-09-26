from generate import *


def main():
    print( "Welcome to the static site generator!" )
    print("Cleaning public directory")
    clean_dir_content("public")
    print( "static to public generation" )
    static_log = tree_copy("static", "public")
    print(static_log)
    print("site generation")
    site_log = generate_site("content", "template.html", "public")
    # generate_page("content/index.md", "template.html", "public/index.html")
    print(site_log)

if __name__ == "__main__":
    main()
