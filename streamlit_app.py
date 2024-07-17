import os
import time
import streamlit as st


class Finder:
    def __init__(self, search_directory=None, file_type='*'):
        self.search_directory = search_directory
        self.file_type = file_type
        self.indexed_files = self._index_files()

    def _index_files(self):
        files_list = []
        if self.search_directory is None or self.search_directory.strip() == '':
            search_directories = [os.path.expanduser('~')]  # Start search from user home directory
        else:
            search_directories = [self.search_directory]

        for search_directory in search_directories:
            for root, _, files in os.walk(search_directory):
                for file in files:
                    if self.file_type == '*' or self.file_type == '' or file.endswith(f'.{self.file_type}'):
                        file_path = os.path.join(root, file)
                        try:
                            files_list.append(file_path)
                        except PermissionError:
                            st.warning(f"Permission denied: {file_path}")
        return files_list

    def find(self, filename_substr):
        return [file for file in self.indexed_files if filename_substr in file]

    def recent(self, count):
        return self.indexed_files[:count]

    def open_file(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except PermissionError:
            return f"Permission denied: {file_path}"

    def get_file_details(self, file_path):
        try:
            file_size = os.path.getsize(file_path)
            creation_time = time.ctime(os.path.getctime(file_path))
            modification_time = time.ctime(os.path.getmtime(file_path))
            return {
                'File Path': file_path,
                'File Size': file_size,
                'Creation Time': creation_time,
                'Modification Time': modification_time
            }
        except PermissionError:
            return {
                'File Path': file_path,
                'File Size': 'Permission denied',
                'Creation Time': 'Permission denied',
                'Modification Time': 'Permission denied'
            }


def main():
    st.set_page_config(page_title="File Indexer GUI", layout="wide")

    st.title("📂 File Indexer GUI")
    st.markdown("A simple graphical interface to interact with the file indexer.")

    st.sidebar.header("Configuration")

    search_directory = st.sidebar.text_input("Search Directory (leave blank to search entire computer)")
    file_type = st.sidebar.text_input("File Type (leave blank or use * for all types)", value="*")
    find = st.sidebar.text_input("Find (Filename substring)")
    recent = st.sidebar.number_input("Recent (Number of recent files to show)", min_value=0, step=1)
    open_file = st.sidebar.checkbox("Open File")

    st.sidebar.markdown("### Click below to run the file indexer")
    if st.sidebar.button("Run"):
        finder = Finder(search_directory=search_directory, file_type=file_type)

        results = ""

        if find:
            found_files = finder.find(find)
            if found_files:
                for file_path in found_files:
                    details = finder.get_file_details(file_path)
                    results += f"\nFile Path: {details['File Path']}"
                    results += f"\nFile Size: {details['File Size']} bytes"
                    results += f"\nCreation Time: {details['Creation Time']}"
                    results += f"\nModification Time: {details['Modification Time']}\n"
            else:
                results += "No files found with the given substring."

        if recent > 0:
            recent_files = finder.recent(recent)
            if recent_files:
                results += "\nRecent Files:\n"
                for file_path in recent_files:
                    details = finder.get_file_details(file_path)
                    results += f"\nFile Path: {details['File Path']}"
                    results += f"\nFile Size: {details['File Size']} bytes"
                    results += f"\nCreation Time: {details['Creation Time']}"
                    results += f"\nModification Time: {details['Modification Time']}\n"
            else:
                results += "No recent files found."

        if open_file:
            recent_files = finder.recent(1)
            if recent_files:
                results += "\n\nFile Content:\n" + finder.open_file(recent_files[0])
            else:
                results += "No recent files found to open."

        st.markdown("### Results")
        st.text_area("Results", results, height=400)

    st.sidebar.markdown("---")
    st.sidebar.markdown("Developed with ❤️ using [Streamlit](https://streamlit.io/)")


if __name__ == "__main__":
    main()