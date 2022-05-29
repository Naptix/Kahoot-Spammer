import os
import io
import re
import sys
import time
import ctypes
import random
import zipfile

from colorama import Fore
from selenium import webdriver
from distutils.version import LooseVersion
from selenium.webdriver.common.by import By
from urllib.request import urlopen, urlretrieve
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions


def setTitle(title):
    system = os.name
    if system == 'nt':
        ctypes.windll.kernel32.SetConsoleTitleW(f"{title} | Made By Naptix")
    elif system == 'posix':
        sys.stdout.write(f"\x1b]0;{title} | Made By Naptix\x07")
    else:
        pass


def slowprint(s):
    for c in s + '\n':
        sys.stdout.write(c)
        sys.stdout.flush()
        time.sleep(0.06)


def clear():
    system = os.name
    if system == 'nt':
        os.system('cls')
    elif system == 'posix':
        os.system('clear')
    else:
        print('\n'*120)
    return


def validatePin(gamePin):
    print(f'{Fore.GREEN}Checking pin...{Fore.RESET}')
    options = Options()
    options.add_argument("--incognito")
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_experimental_option('detach', True)
    web = webdriver.Chrome(options=options)
    web.get("https://kahoot.it/")

    web.find_element(
        By.XPATH, '//*[@id="game-input"]').send_keys(gamePin)
    web.find_element(
        By.XPATH, '//*[@id="root"]/div[1]/div/div/div/div[3]/div[2]/main/div/form/button').click()

    try:
        if WebDriverWait(web, 5).until(expected_conditions.presence_of_element_located((By.XPATH, '//*[@id="nickname"]'))):
            slowprint(f"{Fore.GREEN}Valid pin{Fore.RESET}")
    except TimeoutException:
        slowprint(f"{Fore.RED}Invalid pin2{Fore.RESET}")
        time.sleep(1)
        __import__("main").main()

    web.quit()


def createBot(driver, gamePin, botName, botCount):
    if botCount >= 2:
        driver.execute_script("window.open('');")
        driver.switch_to.window(driver.window_handles[botCount - 1])

    driver.get('https://kahoot.it')

    WebDriverWait(driver, 10).until(
        expected_conditions.presence_of_element_located(
            (By.XPATH, '//*[@id="game-input"]'))
    )
    driver.find_element(
        By.XPATH, '//*[@id="game-input"]').send_keys(gamePin)
    driver.find_element(
        By.XPATH, '//*[@id="root"]/div[1]/div/div/div/div[3]/div[2]/main/div/form/button').click()

    WebDriverWait(driver, 10).until(
        expected_conditions.presence_of_element_located(
            (By.XPATH, '//*[@id="nickname"]'))
    )
    driver.find_element(
        By.XPATH, '//*[@id="nickname"]').send_keys(botName, botCount)
    driver.find_element(
        By.XPATH, '//*[@id="root"]/div[1]/div/div/div/div[3]/div[2]/main/div/form/button').click()

    print(f"{Fore.GREEN}Added {botName}{botCount}{Fore.RESET}")


google_target_ver = 0


class Chrome_Installer(object):
    installed = False
    target_version = None
    DL_BASE = "https://chromedriver.storage.googleapis.com/"

    def __init__(self, executable_path=None, target_version=None, *args, **kwargs):
        self.platform = sys.platform

        if google_target_ver:
            self.target_version = google_target_ver

        if target_version:
            self.target_version = target_version

        if not self.target_version:
            self.target_version = self.get_release_version_number().version[0]

        self._base = base_ = "chromedriver{}"

        exe_name = self._base
        if self.platform in ("win32",):
            exe_name = base_.format(".exe")
        if self.platform in ("linux",):
            self.platform += "64"
            exe_name = exe_name.format("")
        if self.platform in ("darwin",):
            self.platform = "mac64"
            exe_name = exe_name.format("")
        self.executable_path = executable_path or exe_name
        self._exe_name = exe_name

        if not os.path.exists(self.executable_path):
            self.fetch_chromedriver()
            if not self.__class__.installed:
                if self.patch_binary():
                    self.__class__.installed = True

    @staticmethod
    def random_cdc():
        cdc = random.choices('abcdefghijklmnopqrstuvwxyz', k=26)
        cdc[-6:-4] = map(str.upper, cdc[-6:-4])
        cdc[2] = cdc[0]
        cdc[3] = "_"
        return "".join(cdc).encode()

    def patch_binary(self):
        linect = 0
        replacement = self.random_cdc()
        with io.open(self.executable_path, "r+b") as fh:
            for line in iter(lambda: fh.readline(), b""):
                if b"cdc_" in line:
                    fh.seek(-len(line), 1)
                    newline = re.sub(b"cdc_.{22}", replacement, line)
                    fh.write(newline)
                    linect += 1
            return linect

    def get_release_version_number(self):
        path = (
            "LATEST_RELEASE"
            if not self.target_version
            else f"LATEST_RELEASE_{self.target_version}"
        )
        return LooseVersion(urlopen(self.__class__.DL_BASE + path).read().decode())

    def fetch_chromedriver(self):
        base_ = self._base
        zip_name = base_.format(".zip")
        ver = self.get_release_version_number().vstring
        if os.path.exists(self.executable_path):
            return self.executable_path
        urlretrieve(
            f"{self.__class__.DL_BASE}{ver}/{base_.format(f'_{self.platform}')}.zip",
            filename=zip_name,
        )
        with zipfile.ZipFile(zip_name) as zf:
            zf.extract(self._exe_name)
        os.remove(zip_name)
        if sys.platform != "win32":
            os.chmod(self._exe_name, 0o755)
        return self._exe_name


def getDriver():
    driver = "chromedriver.exe"
    print(f"\n{Fore.GREEN}Checking driver...{Fore.RESET}")
    time.sleep(0.5)

    if os.path.exists(os.getcwd() + os.sep + driver):
        print(f"{Fore.GREEN}{driver} already exists, continuing...{Fore.RESET}")
        time.sleep(0.5)
        return driver
    else:
        print(f"{Fore.RED}Driver not found! Installing it for you")
        Chrome_Installer()
        print(f"{Fore.GREEN}Installing chromedriver.exe{Fore.RESET}")
        return "chromedriver.exe"

# ----- Fade Types -----


def blackwhite(text):
    os.system("")
    faded = ""
    red = 0
    green = 0
    blue = 0
    for line in text.splitlines():
        faded += (f"\033[38;2;{red};{green};{blue}m{line}\033[0m\n")
        if not red == 255 and not green == 255 and not blue == 255:
            red += 20
            green += 20
            blue += 20
            if red > 255 and green > 255 and blue > 255:
                red = 255
                green = 255
                blue = 255
    return faded


def neon(text):
    os.system("")
    fade = ""
    for line in text.splitlines():
        red = 255
        for char in line:
            red -= 2
            if red > 255:
                red = 255
            fade += (f"\033[38;2;{red};0;255m{char}\033[0m")
        fade += "\n"
    return fade


def purple(text):
    os.system("")
    fade = ""
    red = 255
    for line in text.splitlines():
        fade += (f"\033[38;2;{red};0;180m{line}\033[0m\n")
        if not red == 0:
            red -= 20
            if red < 0:
                red = 0
    return fade


def water(text):
    os.system("")
    fade = ""
    green = 10
    for line in text.splitlines():
        fade += (f"\033[38;2;0;{green};255m{line}\033[0m\n")
        if not green == 255:
            green += 15
            if green > 255:
                green = 255
    return fade


def fire(text):
    os.system("")
    fade = ""
    green = 250
    for line in text.splitlines():
        fade += (f"\033[38;2;255;{green};0m{line}\033[0m\n")
        if not green == 0:
            green -= 25
            if green < 0:
                green = 0
    return fade
# ----- Fade Types -----


def getTempDir():
    system = os.name
    if system == 'nt':
        return os.getenv('temp')
    elif system == 'posix':
        return '/tmp/'


def getTheme():
    themes = ["dark", "fire", "water", "neon"]
    with open(getTempDir()+"\\naptix_theme", 'r') as f:
        text = f.read()
        if not any(s in text for s in themes):
            slowprint(
                f'{Fore.RED}[Error]: Invalid theme was given, switching to default...{Fore.RESET}')
            setTheme('neon')
            time.sleep(1)
            __import__("main").main()
        return text


def setTheme(new: str):
    with open(getTempDir()+"\\naptix_theme", 'w') as f:
        f.write(new)


def banner(theme=None):
    if theme == "dark":
        print(bannerTheme(blackwhite, blackwhite))
    elif theme == "fire":
        print(bannerTheme(fire, fire))
    elif theme == "water":
        print(bannerTheme(water, water))
    elif theme == "neon":
        print(bannerTheme(purple, neon))
    else:
        print(f'''{Fore.BLUE}
    ██╗  ██╗ █████╗ ██╗  ██╗ █████╗  █████╗ ████████╗   ██████╗██████╗  █████╗ ███╗   ███╗███╗   ███╗███████╗██████╗
    ██║ ██╔╝██╔══██╗██║  ██║██╔══██╗██╔══██╗╚══██╔══╝  ██╔════╝██╔══██╗██╔══██╗████╗ ████║████╗ ████║██╔════╝██╔══██╗
    █████═╝ ███████║███████║██║  ██║██║  ██║   ██║     ╚█████╗ ██████╔╝███████║██╔████╔██║██╔████╔██║█████╗  ██████╔╝
    ██╔═██╗ ██╔══██║██╔══██║██║  ██║██║  ██║   ██║      ╚═══██╗██╔═══╝ ██╔══██║██║╚██╔╝██║██║╚██╔╝██║██╔══╝  ██╔══██╗
    ██║ ╚██╗██║  ██║██║  ██║╚█████╔╝╚█████╔╝   ██║     ██████╔╝██║     ██║  ██║██║ ╚═╝ ██║██║ ╚═╝ ██║███████╗██║  ██║
    ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚════╝  ╚════╝    ╚═╝     ╚═════╝ ╚═╝     ╚═╝  ╚═╝╚═╝     ╚═╝╚═╝     ╚═╝╚══════╝╚═╝  ╚═╝
    
Made by: Naptix
Discord: Cedric#6202
Github: https://github.com/Naptix
────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
[1] Kahoot Spammer    
[2] Change Theme                            
────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────{Fore.RESET}''')


def bannerTheme(type1, type2):
    return type1(f'''
    ██╗  ██╗ █████╗ ██╗  ██╗ █████╗  █████╗ ████████╗   ██████╗██████╗  █████╗ ███╗   ███╗███╗   ███╗███████╗██████╗
    ██║ ██╔╝██╔══██╗██║  ██║██╔══██╗██╔══██╗╚══██╔══╝  ██╔════╝██╔══██╗██╔══██╗████╗ ████║████╗ ████║██╔════╝██╔══██╗
    █████═╝ ███████║███████║██║  ██║██║  ██║   ██║     ╚█████╗ ██████╔╝███████║██╔████╔██║██╔████╔██║█████╗  ██████╔╝
    ██╔═██╗ ██╔══██║██╔══██║██║  ██║██║  ██║   ██║      ╚═══██╗██╔═══╝ ██╔══██║██║╚██╔╝██║██║╚██╔╝██║██╔══╝  ██╔══██╗
    ██║ ╚██╗██║  ██║██║  ██║╚█████╔╝╚█████╔╝   ██║     ██████╔╝██║     ██║  ██║██║ ╚═╝ ██║██║ ╚═╝ ██║███████╗██║  ██║
    ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚════╝  ╚════╝    ╚═╝     ╚═════╝ ╚═╝     ╚═╝  ╚═╝╚═╝     ╚═╝╚═╝     ╚═╝╚══════╝╚═╝  ╚═╝

Made by: Naptix
Discord: Cedric#6202
Github: https://github.com/Naptix''')+type2('''────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
[1] Kahoot Spammer    
[2] Change Theme                            
────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────''')
