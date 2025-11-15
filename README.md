# Gym Class Booking Automation 🏋️‍♂️

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![Selenium](https://img.shields.io/badge/Selenium-4.0+-green.svg)](https://selenium-python.readthedocs.io/)
[![Status](https://img.shields.io/badge/Status-Active-brightgreen.svg)]()

An automated web scraping tool that books gym classes using Selenium WebDriver. This project is part of the **100 Days of Python** challenge (Day 49).

## 🚀 Features

- **Automated Login**: Logs into the gym booking system automatically
- **Smart Class Detection**: Finds specific classes on designated days (Wednesday, Sunday, Friday)
- **Time-based Filtering**: Targets 6 PM classes specifically
- **Booking Management**: Books available classes or joins waitlists
- **Verification System**: Confirms successful bookings
- **Retry Mechanism**: Handles failures with automatic retries
- **Detailed Reporting**: Provides comprehensive booking summaries

## 📋 Prerequisites

- Python 3.7 or higher
- Chrome browser installed
- ChromeDriver (automatically managed by Selenium)

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/gym-scraping.git
   cd gym-scraping
   ```

2. **Install required packages**
   ```bash
   pip install selenium
   ```

3. **Set up Chrome profile** (optional)
   - The script creates a `chrome_profile` directory for persistent browser data
   - This helps maintain login sessions between runs

## 🎯 Usage

### Basic Usage

```python
python main.py
```

### Configuration

Update the login credentials in the `login()` function:

```python
email.send_keys("your-email@example.com")
password.send_keys("your-password")
```

Modify target days in the main function:
```python
days_num_list = find_tuesday(driver, days_heading, ['wed', 'sun', 'fri'])
```

## 📁 Project Structure

```
Day_49_Gym_Scraping/
├── main.py              # Main scraping script
├── chrome_profile/       # Chrome browser profile data
├── .gitignore           # Git ignore file
└── README.md            # Project documentation
```

## 🔧 Key Functions

| Function | Description |
|----------|-------------|
| `setup_driver()` | Configures Chrome WebDriver with custom options |
| `login()` | Handles automated login process |
| `find_tuesday()` | Locates specific days in the schedule |
| `find_6pm_class()` | Filters classes by time (6 PM) |
| `wait_for()` | Waits for elements to load with various conditions |
| `retry()` | Decorator for retry logic on failed operations |

## 📊 Output Example

```
Already Booked for: Yoga Class on Wed, 15 Jan
Booked a Class: HIIT Training on Fri, 17 Jan
Waitlisted for: Pilates on Sun, 19 Jan

-------------Booking Summary-------------
   New Bookings: 1
   Waitlists joined: 1
   Already Booked/Waitlisted: 1
   Total Classes Scheduled: 3

---------------New Bookings---------------
   [New Booking] HIIT Training Fri, 17 Jan
   [Waitlist Joined] Pilates Sun, 19 Jan

------------Verified Bookings--------------
   [Verified] HIIT Training on Fri, 17 Jan
   [Verified] Pilates on Sun, 19 Jan
   
   All Bookings Verified!
```

## ⚙️ Configuration Options

### WebDriver Options
- **Window Size**: 1920x1080 (configurable)
- **User Data Directory**: Persistent Chrome profile
- **Detach Mode**: Browser stays open after script completion

### Retry Settings
- **Default Retries**: 7 attempts
- **Timeout**: 10 seconds for element waiting

## 🚨 Important Notes

- **Demo Site**: Currently configured for `https://appbrewery.github.io/gym/`
- **Test Credentials**: Uses demo credentials (`student@test.com` / `password123`)
- **Chrome Profile**: Automatically created in project directory
- **Rate Limiting**: Built-in delays to avoid overwhelming the server

## 🛡️ Error Handling

The script includes comprehensive error handling:
- Retry mechanism for failed clicks
- Element waiting with timeouts
- Alert handling for unexpected popups
- Graceful failure reporting

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 🏷️ Tags

`python` `selenium` `web-scraping` `automation` `gym-booking` `100-days-of-python` `webdriver` `chrome` `booking-system` `waitlist` `scheduling`

## 📞 Support

If you encounter any issues or have questions:
- Open an issue on GitHub

## 🎓 Learning Objectives

This project demonstrates:
- Web automation with Selenium
- Error handling and retry mechanisms
- DOM manipulation and element waiting
- Data extraction and processing
- User session management
- Automated testing concepts

---

**Part of the 100 Days of Python Challenge - Day 49** 🐍