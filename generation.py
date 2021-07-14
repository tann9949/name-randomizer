from typing import List, Tuple, Dict
import random

import numpy as np


def random_phonenum() -> str:
    """
    Random phone number where
        - first digits always start with 0
        - second digit can be either 6, 8, or 9
        - maximum of 10 digits

    Return
    ------
    phonenum: str
        Randomized phone number
    """
    digit_rand: str = ''.join([str(int(random.random()*10)) for _ in range(8)])
    second_digit: int = random.choice([6, 8, 9])
    phone_num: str = '0{}{}'.format(second_digit, digit_rand)
    return phone_num


def random_homenum() -> str:
    """
    Random house address number in Thai format {XXX}/{XXX}

    Return
    ------
    house_num: str
        Randomed house number
    """
    if random.random() > 0.5:
        return str(int(random.random()*150))+'/'+str(int(random.random()*150))
    else:
        return str(int(random.random()*20))


def random_addr(amphoes: List[str], districts: List[str], provinces: List[str], zipcodes: List[str]) -> str:
    """
    Random Thai address using provided list of `amphoes`, `districts`, `provinces` and `zipcode`

    Arguments
    ---------
    amphoes: List[str]
        List of amphoes in Thailand
    districts: List[str]
        List of districts in Thailand
    provinces: List[str]
        List of Thai provinces
    zipcodes: List[str]
        List of Thai zipcodes

    Return
    ------
    address: str
        Randomized address picked form combinations of provided amphoes, districts, provinces, and zipcodes
    """
    prefix: Tuple[str, str] = random.choice([('ตำบล', 'อำเภอ'), ('แขวง', 'เขต')])
    rand_homenum: str = random_homenum()
    rand_amphoe: str = random.choice(amphoes)
    rand_district: str = random.choice(districts)
    rand_prov: str = random.choice(provinces)
    rand_zip: str = random.choice(zipcodes)
    return f"บ้านเลขที่ {rand_homenum} {prefix[0]}{rand_amphoe} {prefix[1]}{rand_district} จังหวัด{rand_prov} {rand_zip}"


def random_name(first_names: List[str], last_names: List[str], p_pronoun: float = 0.0) -> str:
    """
    Random name using prefix from
    https://www.stou.ac.th/thai/grad_stdy/Apply/prefix.asp

    name are randomed from list of first names and last names (`first_names`, `last_names`)

    Arguments
    ---------
    first_names: List[str]
        List of first names to random on
    last_names: List[str]
        List of last names to choose
    p_pronoun: float
        Probability of adding pronoun

    Return
    ------
    name: str
        Randomized name from provided first_names, and last_names
    """
    pronouns: Dict[str, str] = {"male": ["กระผม", "ผม"], "female": ["หนู", "ดิฉัน"]};
    normal_prefix: Dict[str, str] = {"male": ["เด็กชาย", "นาย"], "female": ["เด็กหญิง", "นาง", "นางสาว"]};
    advance_prefix: List[str] = ["หม่อมหลวง", "บาทหลวง", "หม่อมราชวงศ์",
                      "พลเอก", "พลตรี", "พันโท", "ร้อยเอก", "ร้อยตรี", "จ่าสิบโท", "สิบเอก", "สิบตรี", 
                      "พลโท", "พันเอก", "พันตรี", "ร้อยโท", "จ่าสิบเอก", "จ่าสิบตรี", "สิบโท", "พลทหาร", 
                      "พลอากาศเอก", "พลอากาศตรี", "นาวาอากาศโท", "เรืออากาศเอก", "เรืออากาศตรี", "พันจ่าอากาศโท", "จ่าอากาศเอก", "จ่าอากาศตรี", 
                      "พลอากาศโท", "นาวาอากาศเอก", "นาวาอากาศตรี", "เรืออากาศโท", "พันจ่าอากาศเอก", "พันจ่าอากาศตรี", "จ่าอากาศโท",
                      "พลตำรวจเอก", "พลตำรวจตรี", "พันตำรวจโท", "ร้อยตำรวจเอก", "ร้อยตำรวจตรี", "นายดาบตำรวจ", "สิบตำรวจเอก", 
                       "พลตำรวจโท", "พันตำรวจเอก", "พันตำรวจตรี", "ร้อยตำรวจโท", "จ่าสิบตำรวจ", "สิบตำรวจตรี", "สิบตำรวจโท", "พลตำรวจ", ]

    use_advance: int = np.random.choice([1, 0], size=1, p=[0.2, 0.8])[0];
    gender, prefix = ("male", random.choice(normal_prefix["male"])) if random.random() > 0.5 else ("female", random.choice(normal_prefix["female"]));
    if use_advance:
        prefix: str = random.choice(advance_prefix);

    template: str = f"{prefix} {random.choice(first_names)} {random.choice(last_names)}";

    # if include pronoun add pronoun in front
    if random.random() < p_pronoun:
        pronoun: str = random.choice(pronouns[gender]);
        template = f"{pronoun} {template}";

    return template;