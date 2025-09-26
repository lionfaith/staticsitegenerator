from generate import *
import sys

def main():
    target_dir = "docs"

    print( "Welcome to the static site generator!" )
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"

    print(f"Cleaning {target_dir} directory")
    clean_dir_content(target_dir)

    print( f"static to {target_dir} generation" )
    static_log = tree_copy("static", target_dir)
    print(static_log)
    
    print("site generation")
    site_log = generate_site("content", "template.html", target_dir, basepath)
    print(site_log)

if __name__ == "__main__":
    main()
