import requests
from bs4 import BeautifulSoup


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


def main():
    username = input("Enter a GitHub username: ")
    user_info = scrape_github_user_info(username)

    if user_info:
        bio, repo_count, pull_requests, stars = user_info
        print(f"Bio: {bio}")
        print(f"Number of Repositories: {repo_count}")
        print(f"Number of Pull Requests: {pull_requests}")
        print(f"Number of Stars: {stars}")
    else:
        print("User not found or an error occurred.")


if __name__ == "__main__":
    main()
