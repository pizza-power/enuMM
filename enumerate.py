#!/usr/bin/env python3
#
# Title:enuMM
#
# Author: pizzapower - Matthew Moreschi (where the MM comes from)
#
# A bug bounty enumeration script.
#
# basic operations
# pizza-enum.py --header "reasearcher: pizzapower" --threads 2 --input-file domains.txt --blacklist blacklist.txt
#
# or for a single domain
# pizza-enum.py --domain pizzapower.me
#
# MVP == Refactor
# Pass argparse object to each function then just run them as you want
# run_amass()


import argparse
import sys
import os
import subprocess
from shutil import which
from colorama import init, Fore, Style
import pyfiglet

init(autoreset=True)


def printBanner():

    banner = pyfiglet.figlet_format("enuMMv0.2")
    print(banner)
    return


def pos_print(text: str):
    """
    :param text: function to print a green plus sign in brackets if the outcome
    of whatever code is favorable
    """
    print("\n" + Fore.GREEN + "[+] " + Style.RESET_ALL + text)


def neg_print(text: str):
    """
    :param text: function to print a red minus sign in brackets if the outcome
    of whatever code is not favorable
    """
    print("\n" + Fore.RED + "[-] " + Style.RESET_ALL + text)


# parse the CLI arguments
def parse_args():
    parser = argparse.ArgumentParser()
    # proxy
    parser.add_argument(
        "-p", "--proxy", help="proxy to be used e.g. burp '127.0.0.1:9090'"
    )

    # group -d and -l
    domain_group = parser.add_mutually_exclusive_group(required=True)
    # single domain
    domain_group.add_argument(
        "-d",
        "--domain",
        help="enumerates a single domain e.g. '-d pizzapower.me'",
    )
    # multiple domains from a list
    domain_group.add_argument(
        "-l", "--domains", help="loads a list of domains from a list"
    )

    # blacklist
    parser.add_argument(
        "-b", "--blacklist", help="a list of domains to ignore"
    )

    # output file
    parser.add_argument(
        "-o",
        "--output",
        help="creates main directory where all this enum will be stored",
    )
    # number of threads to use
    parser.add_argument("-t", "--threads", help="number of threads to use")
    # headers to add
    parser.add_argument("--headers", help="custom header to use")

    parser.add_argument(
        "--continuous",
        help="runs this script continuously and notifies user of new subdomains",
    )

    args = parser.parse_args()

    return args


def check_dependencies(dependency_list: list):
    """this check for amass, httpx, and other tools to
    ensure they are installed before running script
    returns true or false with exception
    """
    do_they_exist = [
        program for program in dependency_list if which(program) is not None
    ]
    shit_you_dont_have_installed = list(
        set(dependency_list) ^ set(do_they_exist)
    )
    if shit_you_dont_have_installed:
        neg_print(
            "The following programs are not in $PATH. Please install them: "
            + str(shit_you_dont_have_installed)
        )
        sys.exit(-1)
    return


def run_amass(domain: str):
    pos_print(f"Running amass on: {domain}")
    try:
        filename = f"{domain}/amass-{domain}.txt"
        subprocess.call(
            [
                "amass",
                "enum",
                "-ip",
                "-v",
                "-config",
                "/home/pizzapower/configs/amass.cfg",
                "-d",
                domain,
                "-o",
                filename,
            ]
        )
    except Exception as e:
        neg_print(e)
    return


def run_eyewitness(domain: str):
    # set a useragent
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"
    timeout = 10
    delay = 2  # delay from opening
    threads = 1  # get from threads option at start

    output_directory = f"{domain}/eyewitness"
    os.mkdir(output_directory)

    command = f"~/tools/EyeWitness/Python/EyeWitness.py --web -f {domain}/httpx-{domain}.txt -d {output_directory} --no-prompt --delay {delay} --timeout {timeout}"

    try:
        os.system(command)
    except Exception as e:
        neg_print(e)
    return


def run_httpx(domain: str):
    pos_print(f"Running httpx on: {domain}")
    # httpx -ports 80,443,8009,8080,8081,8090,8180,8443 -l subdomains.txt -o httpx.txt
    # create subdomains from amass list
    # can maybe do this with just amass and db flag or something
    command = f'cut -d " " -f 2 {domain}/amass-{domain}.txt | tr , "\n" | uniq > {domain}/ips-{domain}.txt'
    try:
        os.system(command)

    except Exception as e:
        neg_print(e)

    try:
        input_filename = f"{domain}/ips-{domain}.txt"
        output_filename = f"{domain}/httpx-{domain}.txt"

        subprocess.call(
            [
                "httpx",
                "-ports",
                "80,443,8009,8080,8081,8090,8180,8443",
                "-l",
                input_filename,
                "-o",
                output_filename,
            ]
        )
    except Exception as e:
        neg_print(e)
    return


def search_blacklist(domain: str):
    return


def masscan_or_nmap(ip_address: str):
    return


def find_new_subdomains(domain: str):
    """run this in a loop after init"""
    return


def get_ip_addresses_from_subdomain_list():
    """uses amass ip to get ips from already run scan
    won't need this is we use amass db command
    """

    """
    cut -d " " -f 2 amass-westernunion.com.txt | tr , '\n' | uniq
    """
    return


def get_domains_from_amass_output():
    """opens amass.txt and gets subdomains
    to run them through amass again to
    find sub-sub-domains
    """
    with open("arguments.domains") as domains:
        domain_list = [line.strip() for line in domains]


def main():
    printBanner()
    # check dependencies to make sure you have the proper stuff installed
    # dependency_list = ["amass", "httpx"]
    dependency_list = ["amass"]

    check_dependencies(dependency_list)

    # get the command line arguments
    # eyewitness just passes this to functions
    arguments = parse_args()

    # get the blacklisted domains
    # amass actually has a blacklist option
    # amass enum -blf data/blacklist.txt -d example.com

    if arguments.blacklist:
        try:
            with open(arguments.blacklist) as blacklist:
                blacklisted = [line.strip() for line in blacklist]
                blacklist.close()
        except FileNotFoundError as e:
            neg_print("Blacklist not found in this directory. Exiting!")
            sys.exit(-1)

    # run on a single domain
    if arguments.domain:
        os.mkdir(arguments.domain)
        run_amass(arguments.domain)
        run_httpx(arguments.domain)
        run_eyewitness(arguments.domain)

    # run on a list of domains
    if arguments.domains:
        try:
            with open(arguments.domains) as domains:
                domain_list = [line.strip() for line in domains]
            domains.close()
        except FileNotFoundError as e:
            neg_print("Whitelist not found in this directory. Exiting!")
            sys.exit(-1)

        # need to compare white and black list
        if arguments.blacklist:
            final_domains = [
                domain for domain in domain_list if domain not in blacklisted
            ]
        else:
            final_domains = domain_list

        # thread this
        for domain in final_domains:
            # mkdir then run apps
            os.mkdir(domain)
            run_amass(domain)
            run_httpx(domain)
            run_eyewitness(domain)

    sys.exit()


if __name__ == "__main__":
    main()
