from selenium import webdriver
import time,os,re
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import UnexpectedAlertPresentException


def retry(func,retries=7,description=''):
    def wrapper(*args, **kwargs):
        attempt= 1
        while attempt<=retries:
            result=func(*args, **kwargs)
            if result==1:
                print(f'successfully {description} on attempt {attempt}.')
                return
            else:
                print(f'Error {description} on attempt {attempt}: {result}')
                attempt+=1
        return

    return wrapper

def wait_for(driver, by, selector, condition="visible", timeout=10, multiple=False):
    """
    Waits for one or more elements to meet a condition before continuing.

    Args:
        driver: Selenium WebDriver instance.
        by: selenium.webdriver.common.by.By (e.g., By.ID, By.CSS_SELECTOR).
        selector: The element locator string.
        condition: "visible", "present", or "clickable".
        timeout: Max wait time in seconds.
        multiple: If True, returns a list of matching elements. If False, returns a single element.

    Returns:
        WebElement or list[WebElement] that met the condition.
    """
    if multiple:
        conditions_map = {
            "visible": EC.visibility_of_all_elements_located((by, selector)),
            "present": EC.presence_of_all_elements_located((by, selector)),
        }
    else:
        conditions_map = {
            "visible": EC.visibility_of_element_located((by, selector)),
            "present": EC.presence_of_element_located((by, selector)),
            "clickable": EC.element_to_be_clickable((by, selector)),
        }

    if condition not in conditions_map:
        raise ValueError(f"Unknown condition: {condition}")

    return WebDriverWait(driver, timeout).until(conditions_map[condition])

def login(driver):
    button = driver.find_element(By.XPATH, "//*[@id=\"login-button\"]")
    button.click()
    email = wait_for(driver, By.XPATH, "//*[@id=\"email-input\"]", 'visible', 10)
    email.clear()
    email.send_keys("student@test.com")
    password = wait_for(driver, By.XPATH, "//*[@id=\"password-input\"]", 'visible', 10)
    password.clear()
    password.send_keys("password123")
    login = wait_for(driver, By.XPATH, "//*[@id=\"submit-button\"]", 'visible', 10)
    clicking_by_url(driver, login)

def find_tuesday(driver,days_heading,days):
    return_list=[]
    for item in days:
        for i, day in enumerate(days_heading):
            if day.text.split(',')[0][-3:].lower() == item.lower():
                return_list.append(i)
    return return_list

def find_6pm_class(driver,classes_on_tuesday):
    classes=[]
    for i, items in enumerate(classes_on_tuesday):
        start = items.get_attribute('data-class-id')
        hour = start.split('-')[-1]
        if hour == '1800':
            classes.append(i)
    return classes

def setup_driver():
    user_data_dir = os.path.join(os.getcwd(), "chrome_profile")

    driver_options = webdriver.ChromeOptions()

    driver_options.add_argument("--window-size=1920,1080")
    driver_options.add_argument(f"--user-data-dir={user_data_dir}")
    driver_options.add_experimental_option('detach', True)

    driver = webdriver.Chrome(options=driver_options)

    return driver

def print_summary(already,waitlisted,booked,total):

    print(f"\n\n\n\n")
    print(f"-------------Booking Summary-------------")
    print(f"   New Bookings: {booked}")
    print(f"   Waitlists joined: {waitlisted}")
    print(f"   Already Booked/Waitlisted: {already}")
    print(f"   Total Classes Scheduled: {total}")
    print('\n')

def print_new_booking(booked_info,waitlisted_info,booked,waitlisted):
    print(f"---------------New Bookings---------------")
    if booked != 0:
        for item in booked_info:
            info=' '.join(item)
            print(f'   [New Booking]{info}')
    if waitlisted != 0:
        for item in waitlisted_info:
            info=' '.join(item)
            print(f'   [Waitlist Joined]{info}')
    elif waitlisted == 0 and booked == 0:
        print(f'   No New Bookings!')
    print('\n')

def print_verification(driver,total,booked_info,waitlisted_info):
    verified=0

    print(f"------------Verified Bookings--------------")
    bookings_page = wait_for(driver, By.XPATH, "//*[@id=\"my-bookings-link\"]", 'visible', 10)
    bookings_page.click()
    bookings= [item for item in wait_for(driver, By.CLASS_NAME, 'MyBookings_bookingCard__VRdrR', 'visible', 10, True)]
    # bookings.append(item for item in wait_for(driver, By.CLASS_NAME, 'MyBookings_section__oBwNg', 'visible', 10, True))
    name_date_dict={
        'names':[
            wait_for(items, By.CSS_SELECTOR, "h3", 'visible', 10).text for items in bookings
        ],
        'dates':[
            ' '.join(wait_for(items, By.CSS_SELECTOR, "p", 'visible', 10, False).text.split(' ')[1:4]).strip(',') for items in bookings
        ]
    }
    for item in booked_info + waitlisted_info :
        name=item[1]
        date=item[2]
        if name in name_date_dict['names'] and date in name_date_dict['dates']:
            print(f'   [Verified]{name} on {date}')
            verified += 1
        else:
            print(f'   [Not Verified]{name} on {date}')
    if verified == len(booked_info)+len(waitlisted_info):
        print(f'\n   All Bookings Verified!')
    else:
        print(f'\n   Total Bookings Verified: {verified}')

@retry
def clicking_by_url(driver,button):
    old_url = driver.current_url
    button.click()
    time.sleep(2)
    if driver.current_url == old_url:
        return ("Failed.")
    else:
        return 1

@retry
def clicking_by_name(button):
    before=button.text.lower()
    button.click()
    time.sleep(3)
    after=button.text.lower()
    if before == after:
        return 'Failed'
    else:
        return 1

def scrape_example(url):
    driver=setup_driver()
    driver.get(url)

    login(driver)
    booked=0
    waitlisted=0
    already=0
    classes_dates=[]
    classes_names=[]
    class_days=[]
    classes=[]
    booked_info=[]
    waitlisted_info=[]
    already_info=[]

    time.sleep(5)
    days_heading = driver.find_elements(By.CSS_SELECTOR, ".Schedule_dayGroup__y79__ h2")
    days=driver.find_elements(By.CSS_SELECTOR, ".Schedule_dayGroup__y79__")
    days_num_list=find_tuesday(driver,days_heading,['wed','sun','fri'])

    #Update date list and gets the html for the days mentioned using the ids stored in days_num_list
    for day in days_num_list:
        raw_date=days_heading[day].text
        clean_date = re.sub(r"^(Today|Tomorrow)\s*\(|\)$", "", raw_date)
        classes_dates.append(clean_date)
        day_id=days[day].get_attribute("id")
        class_days.append(wait_for(driver, By.ID, f"{day_id}",'visible', 10,False))

    #Updates classes list with classes found in specific days stored in class_days list
    for class_day in class_days:
        temp=class_day.find_elements(By.CLASS_NAME,'ClassCard_card__KpCx5')
        for item in temp:
            classes.append(item)

    #Updates class_name list with booking of classes and prints the info
    classes_num=find_6pm_class(driver, classes)
    for i,item in enumerate(classes_num):
        class_name=wait_for(classes[item], By.CSS_SELECTOR, "h3",'visible',10).text
        button=wait_for(classes[item], By.CSS_SELECTOR, "button",'visible',10)
        classes_names.append(class_name)
        if button.text=='Booked':
            print(f"Already Booked for: {class_name} on {classes_dates[i]}")
            already_info.append(('Already',class_name,classes_dates[i]))
            already+=1
        elif button.text=='Waitlisted':
            print(f"Already Waitlisted for: {class_name} on {classes_dates[i]}")
            already_info.append(('Already',class_name,classes_dates[i]))
            already+=1
        elif button.text=='Join Waitlist':
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", button)
            clicking_by_name(button)
            waitlisted+=1
            waitlisted_info.append(('Waitlisted',class_name,classes_dates[i]))
            print(f"Waitlisted for: {class_name} on {classes_dates[i]}")
        elif button.text=='Book Class' :
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", button)
            clicking_by_name(button)
            booked+=1
            booked_info.append(('Booked',class_name,classes_dates[i]))
            print(f"Booked a Class on Tuesday: {class_name} on {classes_dates[i]}")

    total = already + waitlisted + booked
    print_summary(already,waitlisted,booked,total)

    print_new_booking(booked_info,waitlisted_info,booked,waitlisted)

    print_verification(driver,total,booked_info,waitlisted_info)




if __name__ == "__main__":
    scrape_example("https://appbrewery.github.io/gym/")

