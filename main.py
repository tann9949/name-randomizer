from typing import List
import argparse
import random

from tqdm import tqdm

from data_prep import get_name_df, get_addrs_items
from generation import random_name, random_addr, random_phonenum

address_templates: List[str] = ["อาศัยอยู่ที่", "ที่อยู่", "อยู่ที่"];
phone_templates: List[str] = ["เบอร์โทรศัพท์", "โทร", "เบอร์โทร", "ติดต่อเบอร์"];


def run_parser() -> argparse.Namespace:
    """
    Run argument parsers

    Return
    ------
    args: argparse.Namespace
        Arguments of the programs
    """
    parser = argparse.ArgumentParser(description="Random name and address that MIGHT not really exists using Thai name/address database");
    parser.add_argument("--n-sentences", type=int, default=500, help="Number of randomized sentence");
    parser.add_argument("--out-file", type=str, default="randomized_sentences.txt", help="Output file name");
    parser.add_argument("--p-pronoun", type=float, default=0.0, help="Probability of adding pronoun in front of sentences");
    return parser.parse_args();


def generate_sentences(name: str, addr: str, address_templates: List[str], phone_templates: List[str]) -> str:
    """
    Generate utterance specifying his name, address and phone number. Name and address must be provided
    in advance while other sentence words are randomly generated from provided `pronoun_list`, `address_templates`, and `phone_templates`.
    Phone number are randomly generated. 
    
    The template is formatted as followed:
    '{pronoun} {name} {addr_prefix} {addr} {phone_prefix} {phone}'

    Arguments
    ---------
    name: str
        Name of people to used in utterance
    addr: str
        Address of people to used in utterance
    pronoun_list: List[str]
        List of words to use before name
    address_templates: List[str]
        List of words to use after specifying name and address
    phone_templates: List[str]
        List of words to use after address and before randomed phone number

    Return
    ------
    randomed_sentence: str
        Randomed sentence with using provided templates, name, and address
    """
    # prepare randomized items for template
    addr_prefix: str = random.choice(address_templates);
    phone_prefix: str = random.choice(phone_templates);
    phone: str = random_phonenum();

    # pack template with randomized item and return
    template: str = f"{name} {addr_prefix} {addr} {phone_prefix} {phone}";
    return template;


def main(args: argparse.Namespace) -> None:
    # read from parser
    n_sentences: int = args.n_sentences;
    out_path: str = args.out_file;
    p_pronoun: float = args.p_pronoun;

    with open(out_path, "w") as f:
         # clear out_path if out_path exists
        f.write("");

        # get list of names and addresses
        first_names, last_names = get_name_df();
        provinces, amphoes, districts, zipcodes = get_addrs_items();

        for _ in tqdm(range(n_sentences)):
            # random name and address and generate sentence
            name: str = random_name(first_names, last_names, p_pronoun=p_pronoun);
            addr: str = random_addr(amphoes, districts, provinces, zipcodes);
            sentence: str = generate_sentences(name, addr, address_templates, phone_templates);

            # write randomed sentence to out_path
            f.write(sentence+"\n");


if __name__ == "__main__":
    args = run_parser();
    main(args);
