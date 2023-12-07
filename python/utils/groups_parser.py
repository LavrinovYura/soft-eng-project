import requests
from bs4 import BeautifulSoup


def parse_group_numbers():
    url = "https://ruz.spbstu.ru"

    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        institute_links = soup.find_all('a', class_='faculty-list__link')
        all_group_numbers = []

        for link in institute_links:
            institute_url = url + link['href']
            institute_response = requests.get(institute_url)

            if institute_response.status_code == 200:
                institute_soup = BeautifulSoup(institute_response.text, 'html.parser')
                group_elements = institute_soup.find_all('a', class_='groups-list__link')
                group_numbers = [group.text.strip() for group in group_elements]
                all_group_numbers.extend(group_numbers)
            else:
                print(f"Ошибка при запросе института {institute_url}: {institute_response.status_code}")

        return all_group_numbers
    else:
        print(f"Ошибка при запросе главной страницы: {response.status_code}")


groups = parse_group_numbers()


def is_group_in_list(group_to_check):
    return group_to_check in groups
