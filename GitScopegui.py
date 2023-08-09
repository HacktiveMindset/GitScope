import requests
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import ttk, messagebox


def scrape_github_user_info(username):
    url = f'https://github.com/{username}'
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        bio_element = soup.find('div', class_='p-note user-profile-bio')
        bio = bio_element.get_text().strip() if bio_element else "Bio not available"

        repo_count = soup.find('span', class_='Counter').get_text().strip()

        pull_requests_element = soup.find('a', href=f'/{username}?tab=public-activity')
        pull_requests = pull_requests_element.find('span',
                                                   class_='text-bold text-gray-dark').get_text().strip() if pull_requests_element else "N/A"

        stars = soup.find_all('a', class_='UnderlineNav-item')[1].find('span', class_='Counter').get_text().strip()

        return bio, repo_count, pull_requests, stars
    else:
        return None


def get_user_info():
    username = entry_username.get()
    user_info = scrape_github_user_info(username)

    if user_info:
        bio, repo_count, pull_requests, stars = user_info
        result_text.config(state=tk.NORMAL)
        result_text.delete("1.0", tk.END)
        result_text.insert(tk.END, f"Bio: {bio}\n")
        result_text.insert(tk.END, f"Number of Repositories: {repo_count}\n")
        result_text.insert(tk.END, f"Number of Pull Requests: {pull_requests}\n")
        result_text.insert(tk.END, f"Number of Stars: {stars}\n")
        result_text.config(state=tk.DISABLED)
    else:
        messagebox.showerror("Error", "User not found or an error occurred.")


# Create the main window
root = tk.Tk()
root.title("GitHub User Insights")

# Set a theme for the application
style = ttk.Style()
style.theme_use("clam")

# Add a description label
label_description = ttk.Label(root, text="Retrieve GitHub user information:")
label_description.pack(pady=10)

# Custom font for the "Enter GitHub Username:" label
custom_font = ("Arial", 12)  # Customize the font here
label_username = ttk.Label(root, text="Enter GitHub Username:", font=custom_font)
label_username.pack()

entry_username = ttk.Entry(root)
entry_username.pack()

button_get_info = ttk.Button(root, text="Get Info", command=get_user_info)
button_get_info.pack()

result_text = tk.Text(root, height=10, width=50, state=tk.DISABLED)
result_text.pack(pady=10)

# Add a quit button
button_quit = ttk.Button(root, text="Quit", command=root.quit)
button_quit.pack()

root.mainloop()
