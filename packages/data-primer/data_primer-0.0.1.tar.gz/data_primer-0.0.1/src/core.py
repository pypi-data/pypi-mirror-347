from pandas import DataFrame


def pop_columns(df: DataFrame, headers: List[str]):
    for header in headers:
        if header not in df.columns:
            raise ValueError(f"Header '{header}' not found in DataFrame columns.")
        df.pop(header)


def replace_values(df: DataFrame, headers: List[str], num: int = 1, target: str = 'Other'):
    """
    Used to merge enumeration members with counts less than a threshold in an enumeration column

    df: DataFrame
    headers: The header of the column to be processed
    num: The threshold value, data with counts below this value will be modified uniformly
    target: The value to be replaced with, default is 'Other'

    Example:
        df = pd.DataFrame({'A': ['a', 'a', 'b']})
        replace_values(df, ['A'], num=1, target='c')

        result:
             A
        0    a
        1    a
        2    c
    """

    for header in headers:
        counts = df[header].value_counts()
        values = counts[counts <= num].index.tolist()

        df[header] = df[header].replace(values, target)


def fuzzy_existence(df: DataFrame, headers: List[str], special_value: List[str] = []):
    """
    Converting data in columns to 0/1 form, 0 means no data, 1 means data exists

    df: DataFrame
    headers: The header of the column to be processed
    special_value: Values that will be specially treated as 0

    Example:
        df = pd.DataFrame({'A': ['a', 'np.nan', '', 'd']})
        fuzzy_existence(df, ['A'], remove=['d'])

        result:
             A
        0    1
        1    0
        2    0
        3    0
    """

    for header in headers:
        if remove:
            df[header] = df[header].replace(remove, np.nan)
        df[header] = (~df[header].isna() & (df[header] != '')).astype(int)


def pave(df: DataFrame, headers: List[str], sep: str = ",", case_sensitive: bool = False):
    """
    Extending get_dummies. Split cell contents by sep and expand into columns, and indicate the data situation with 0/1
    Note: The original column will be deleted.

    df: DataFrame.
    headers: The header of the column to be processed.
    sep: The separator used to split the cell contents, default is ",".
    case_sensitive: Whether to distinguish between upper and lower case, default is False.

    Example:
        df = pd.DataFrame({'A': ['a,b,c', 'a,d', "c", 'b,c,d']})
        pave(df, ['A'], sep=',', case_sensitive=False)

        result:
            A_a        A_b        A_c        A_d
        0   1          1          1          0
        1   1          0          0          1
        2   0          0          1          0
        3   0          1          1          1
    """

    for header in headers:
        if not case_sensitive:
            dummies = (
                df[header].str.lower().str.replace(" ", "").str.get_dummies(sep=sep)
            )  # remove space and convert to lowercase
        else:
            dummies = df[header].str.replace(" ", "").str.get_dummies(sep=sep)

        dummies.columns = [f"{header}_{c}" for c in dummies.columns]  # rename headers

        df.pop(header)
        df[dummies.columns] = dummies
