import pandas
import re

def extract_postcode_from_address(addr: str, raiseFailures: bool = True) -> tuple[str, str]:
  try:
    postcode_pattern = re.compile(r'[A-Za-z]{1,2}\d[A-Za-z\d]?\s?\d[A-Za-z]{2}')
    match = postcode_pattern.search(addr)
    postcode = match.group()
    new_addr = addr.replace(postcode, '').rstrip(', \n\t')
    return new_addr, postcode
  except Exception as e:
    if raiseFailures:
      raise Exception(f"unable to extract postcode from address '{addr}', {e}")
    return addr, None

def extract_postcode_from_address_series(s: pandas.Series) -> tuple[str, str]:
  return pandas.Series(extract_postcode_from_address(s['address_1'], False))

def extract_full_name(full_name: str) -> tuple[str, str]:
  full_name = full_name.strip()
  pattern = re.compile(r"^(Mrs|Mr|Ms|Miss|Dr)\.?\s*", re.IGNORECASE)
  full_name = re.sub(pattern, "", full_name)
  parts = full_name.split()
  first_name = parts[0]
  last_name = parts[len(parts)-1].strip()
  if last_name == '' or len(parts) == 1: last_name = None
  return first_name, last_name

def extract_full_name_from_series(s: pandas.Series, key: str) -> tuple[str, str]:
  return pandas.Series(extract_full_name(s[key]))

def extract_full_name_from_df(df: pandas.DataFrame) -> pandas.DataFrame:
  for scenario in ['full_name', 'forename_surname']:
    if scenario in df.columns:
      df[['forename', 'surname']] = df.apply(lambda s: extract_full_name_from_series(s, scenario), axis=1)
      df.drop(columns=[scenario], inplace=True)
  return df

def break_out_individuals_cpl(
    df: pandas.DataFrame,
    header_map: dict, 
    additional_columns: list) -> pandas.DataFrame:
  """
  Variation: Complainant, Partner, Landlord.

  After receiving A.I. intelligence in the form of header_map, 
  we will rename the dataframe for you and break out the possible
  Complainant, Partner and Landlord individuals so the dataframe returned
  is one row per individual (with a row_type column added). 
  
  Some dataframes need additional columns for meta-data, which you can
  include too.

  We will not modify your dataframe passed into this function, making 
  it idempotent.
  """
  
  # rename pii columns
  renamed_df = df.rename(columns=header_map)

  # full name could be a single column
  renamed_df = extract_full_name_from_df(renamed_df)

  # all possible columns we may need to include
  extras = additional_columns if additional_columns is not None else []
  claimant_columns = extras + ['unique_id', 'nino', 'surname', 'forename', 'date_of_birth', 'address_1', 'address_2', 'address_3', 'postcode']
  partner_columns = extras + ['unique_id', 'partner_nino', 'partner_surname', 'partner_forename', 'partner_date_of_birth', 'address_1', 'address_2', 'address_3', 'postcode']
  landlord_columns = extras + ['unique_id', 'landlord_nino', 'landlord_surname', 'landlord_forename', 'landlord_date_of_birth', 'landlord_address_1', 'landlord_address_2', 'landlord_address_3', 'landlord_postcode']
  aa2_columns = extras + ['unique_id', 'aa2_nino', 'aa2_surname', 'aa2_forename', 'aa2_date_of_birth', 'address_1', 'address_2', 'address_3', 'postcode']
  aa3_columns = extras + ['unique_id', 'aa3_nino', 'aa3_surname', 'aa3_forename', 'aa3_date_of_birth', 'address_1', 'address_2', 'address_3', 'postcode']
  aa4_columns = extras + ['unique_id', 'aa4_nino', 'aa4_surname', 'aa4_forename', 'aa4_date_of_birth', 'address_1', 'address_2', 'address_3', 'postcode']

  # build our separate dataframes for each individual
  claimant_df = pandas.DataFrame(columns=claimant_columns)
  partner_df = pandas.DataFrame(columns=partner_columns)
  landlord_df = pandas.DataFrame(columns=landlord_columns)
  aa2_df = pandas.DataFrame(columns=aa2_columns)
  aa3_df = pandas.DataFrame(columns=aa3_columns)
  aa4_df = pandas.DataFrame(columns=aa4_columns)

  # extract relevant columns from the original dataframe
  claimant_df = renamed_df[[col for col in claimant_columns if col in renamed_df]].copy()
  partner_df = renamed_df[[col for col in partner_columns if col in renamed_df]].copy()
  landlord_df = renamed_df[[col for col in landlord_columns if col in renamed_df]].copy()
  aa2_df = renamed_df[[col for col in aa2_df if col in renamed_df]].copy()
  aa3_df = renamed_df[[col for col in aa3_df if col in renamed_df]].copy()
  aa4_df = renamed_df[[col for col in aa4_df if col in renamed_df]].copy()

  # Rename columns to make them consistent
  partner_df = partner_df.rename(columns={ 'partner_nino': 'nino', 'partner_surname': 'surname', 'partner_forename': 'forename', 'partner_date_of_birth': 'date_of_birth' }, errors='ignore')
  landlord_df = landlord_df.rename(columns={ 'landlord_nino': 'nino', 'landlord_surname': 'surname', 'landlord_forename': 'forename', 'landlord_date_of_birth': 'date_of_birth', 'landlord_address_1': 'address_1', 'landlord_address_2': 'address_2', 'landlord_address_3': 'address_3', 'landlord_postcode': 'postcode' }, errors='ignore')
  aa2_df = aa2_df.rename(columns={ 'aa2_nino': 'nino', 'aa2_surname': 'surname', 'aa2_forename': 'forename', 'aa2_date_of_birth': 'date_of_birth' }, errors='ignore')
  aa3_df = aa3_df.rename(columns={ 'aa3_nino': 'nino', 'aa3_surname': 'surname', 'aa3_forename': 'forename', 'aa3_date_of_birth': 'date_of_birth' }, errors='ignore')
  aa4_df = aa4_df.rename(columns={ 'aa4_nino': 'nino', 'aa4_surname': 'surname', 'aa4_forename': 'forename', 'aa4_date_of_birth': 'date_of_birth' }, errors='ignore')

  # mark the differences
  claimant_df['row_type'] = 'claimant'
  partner_df['row_type']  = 'partner'
  landlord_df['row_type'] = 'landlord'
  aa2_df['row_type'] = 'aa2'
  aa3_df['row_type'] = 'aa3'
  aa4_df['row_type'] = 'aa4'

  # concatenate the three dataframes into a single dataframe
  combined_df = pandas.concat([claimant_df, partner_df, landlord_df, aa2_df, aa3_df, aa4_df], axis=0, ignore_index=True)

  # extract postcode from address if it isn't separate
  if 'postcode' not in combined_df.columns:
    combined_df[['address_1', 'postcode']] = combined_df.apply(extract_postcode_from_address_series, axis=1)

  # ensure the required columns
  required_subset = ['forename', 'surname', 'address_1', 'postcode']
  combined_df.dropna(subset=required_subset, inplace=True)
  
  # clean any rogue excel encoding in addresses
  for key in ['address_1', 'address_2', 'address_3', 'postcode']:
    if key in combined_df.columns:
      combined_df[key] = combined_df[key].fillna('').str.replace('_x000D_', ', ')

  # write stats to stdout
  for key in ['claimant', 'partner', 'landlord', 'aa2', 'aa3', 'aa4']:
    subset = combined_df[combined_df['row_type'] == key]
    print(f"{key}: {len(subset)}")
  
  print(f"final tally {len(combined_df)} valid residents")
  return combined_df