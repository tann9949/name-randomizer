from requests.models import Response
from typing import List, Tuple
import requests
import os

import numpy as np
import pandas as pd

firstname_phoneme_path: str = "database/firstname_phoneme.txt"
lastname_phoneme_path: str = "database/lastname_phoneme.txt"
# from https://github.com/Sellsuki/thai-address-database
thai_address_database_path = "database/database.xlsx";


def download_thai_database() -> None:
    """
    Download Thai Address database from source
    https://github.com/Sellsuki/thai-address-database
    """
    download_url: str = "https://github.com/Sellsuki/thai-address-database/blob/master/database/raw_database/database.xlsx?raw=true";
    r: Response = requests.get(download_url, allow_redirects=True);
    with open(thai_address_database_path, "wb") as f:
        f.write(r.content);


def get_addrs_items() -> Tuple[List[str], List[str], List[str], List[str]]:
    """
    Load list of provinces, amphoes, districts and zipcodes in Thailand
    from database

    Returns
    -------
    provinces: List[str]
        List of loaded provinces
    amphoes: List[str]
        List of loaded Amphoes
    districts: List[str]
        List of loaded Districts
    zipcodes: List[str]
        List of loaded zipcodes
    """
    if not os.path.exists(thai_address_database_path):
        download_thai_database();
    db: pd.DataFrame = pd.read_excel(thai_address_database_path);
    provinces: List[str] = sorted(set(db["province"].value_counts().index));
    amphoes: List[str] = sorted(set(db["amphoe"].values));
    districts: List[str] = sorted(set(db["district"].values));
    zipcodes: np.ndarray = np.array(list(set(db["zipcode"].values)));
    zipcodes: np.ndarray = zipcodes[~np.isnan(zipcodes)].astype(int).astype(str).tolist();
    return provinces, amphoes, districts, zipcodes;


def read_phonemes() -> Tuple[List[Tuple[str, str]], List[Tuple[str, str]]]:
    """
    Read firstname, and lastname database including its phoneme

    Returns
    -------
    firstname_phoneme: List[Tuple[str, str]]
        A List of tuple containing first name and its phoneme pronunciation
    lastname_phoneme: List[Tuple[str, str]]
        A List of tuple containing last name and its phoneme pronunciation
    """
    with open(firstname_phoneme_path, "r") as f:
        firstname_phoneme: List[str] = f.readlines();
    firstname_phoneme = [name[:-1] for name in firstname_phoneme];

    with open(lastname_phoneme_path, "r") as f:
        lastname_phoneme: List[str] = f.readlines();
    lastname_phoneme = [name[:-1] for name in lastname_phoneme];

    firstname_phoneme: List[Tuple[str, str]] = [
        (x.split("\t")[0], "\t".join(x.split("\t")[1:])) 
        for x in firstname_phoneme
    ];
    lastname_phoneme: List[Tuple[str, str]] = [
        (x.split("\t")[0], "\t".join(x.split("\t")[1:])) 
        for x in lastname_phoneme
    ];
    return firstname_phoneme, lastname_phoneme


def get_name_df() -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Load firstname, and lastname from database and format into DataFrame

    Returns
    -------
    first_names: List[str]
        List of first name where pronunciation are not duplicated
    last_names: List[str]
        List of last name where pronunciation are not duplicated
    """
    firstname_phoneme, lastname_phoneme = read_phonemes();
    
    firstname_df: pd.DataFrame = pd.DataFrame(firstname_phoneme, columns=["name", "phoneme"]);
    lastname_df: pd.DataFrame = pd.DataFrame(lastname_phoneme, columns=["name", "phoneme"]);

    unique_firstname_df: pd.DataFrame = firstname_df.drop_duplicates(subset=["phoneme"]).sort_values("phoneme").reset_index(drop=True);
    unique_lastname_df: pd.DataFrame = lastname_df.drop_duplicates(subset=["phoneme"]).sort_values("phoneme").reset_index(drop=True);

    first_names: List[str] = unique_firstname_df["name"].values.tolist();
    last_names: List[str] = unique_lastname_df["name"].values.tolist();
    return first_names, last_names;
