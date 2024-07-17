import os
import time
import streamlit as st
from datetime import date, datetime

class Finder:
    def __init__(self, search_directory=None, file_type='*', date_from=None, date_to = None):
        self.search_directory = search_directory
        self.file_type = file_type
        self.date_from = date_from
        self.date_to = date_to
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
                            creation_time = datetime.fromtimestamp(os.path.getctime(file_path))

                            if self.date_from is None or (creation_time >= datetime.combine(self.date_from, datetime.min.time()) and creation_time <= datetime.combine(self.date_to, datetime.max.time())):
                                files_list.append(file_path)
                        except PermissionError:
                            st.warning(f"Permission denied: {file_path}")
                        except OSError:
                            st.warning(f"Error accessing file: {file_path}")
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
        except UnicodeDecodeError:
            return "Cannot display content: Unsupported file format or binary file."

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
    st.set_page_config(page_title="File Indexer and Searcher", layout="wide")

    st.title("📂 File Indexer and Searcher")

    st.sidebar.header("Configuration")

    search_directory = st.sidebar.text_input("Search Directory (leave blank to search entire computer)")
    file_type = st.sidebar.text_input("File Type (leave blank or use * for all types)", value="*")
    find = st.sidebar.text_input("Find (Filename substring)")
    recent = st.sidebar.number_input("Recent (Number of recent files to show)", min_value=0, step=1)
    open_file = st.sidebar.checkbox("Open File")
    date_from = st.sidebar.date_input("Date From", value=date(2020, 1, 1))
    date_to = st.sidebar.date_input("Date To")
    min_size = st.sidebar.number_input("Minimum File Size (bytes)", min_value=0, step=1)
    max_size = st.sidebar.number_input("Maximum File Size (bytes)", min_value=0, step=1)

    if st.sidebar.button("Run"):
        finder = Finder(search_directory=search_directory, file_type=file_type, date_from=date_from, date_to = date_to)

        results = ""

        if find:
            found_files = finder.find(find)
            if found_files:
                results += "Files found with the given substring:\n"
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
        st.text_area("", results, height=400)

if __name__ == "__main__":
    main()
