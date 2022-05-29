from common import *

def main():
    clear()
    if getTheme() == "dark":
        banner("dark")
    elif getTheme() == "fire":
        banner("fire")
    elif getTheme() == "water":
        banner("water")
    elif getTheme() == "neon":
        banner("neon")
    else:
        banner()
    setTitle("Kahoot Spammer")
    choice = input("Choice: ")
    if choice == "1":
        getDriver()
        try:
            gamePin = int(input("Game pin: "))
        except ValueError:
            slowprint(f"{Fore.RED}That isn't a number!{Fore.RESET}")
            time.sleep(1)
            main()
        validatePin(gamePin)
        try:
            botAmount = int(input("How many bots: "))
        except ValueError:
            slowprint(f"{Fore.RED}That isn't a number!{Fore.RESET}")
            time.sleep(1)
            main()
        botName = input(
            "Name of bots (index will be at the end automatically): ")
        botCount = 1

        options = Options()
        options.add_argument("--incognito")
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        options.add_experimental_option('detach', True)
        driver = webdriver.Chrome(options=options)

        for i in range(botAmount):
            createBot(driver, gamePin, botName, botCount)
            botCount += 1
            if botCount > botAmount:
                input("Press enter to quit: ")
                slowprint(f"{Fore.RED}Quiting driver...{Fore.RESET}")
                driver.quit()
                main()
    elif choice == "2":
        print("[1] Dark\n[2] Fire\n[3] Water\n[4] Neon")
        themechoice = input("Choice: ")
        if themechoice == "1":
            setTheme("dark")
            slowprint(f'{Fore.GREEN}Setting theme to dark...{Fore.RESET}')
            time.sleep(1)
            main()
        elif themechoice == "2":
            setTheme("fire")
            slowprint(f'{Fore.GREEN}Setting theme to fire...{Fore.RESET}')
            time.sleep(1)
            main()
        elif themechoice == "3":
            setTheme("water")
            slowprint(f'{Fore.GREEN}Setting theme to water...{Fore.RESET}')
            time.sleep(1)
            main()
        elif themechoice == "4":
            setTheme("neon")
            slowprint(f'{Fore.GREEN}Setting theme to neon...{Fore.RESET}')
            time.sleep(1)
            main()
        else:
            slowprint(f'{Fore.RED}Invalid choice!{Fore.RESET}')
            time.sleep(1)
            main()
    else:
        slowprint(f'{Fore.RED}Invalid choice!{Fore.RESET}')
        time.sleep(1)
        main()


if __name__ == "__main__":
    main()
