import pandas as pd


def indexData(input_path, output_path):
    df = pd.read_csv(input_path)
    df.insert(0, 'tno', range(len(df)))
    df.to_csv(output_path, index=False)


def separateCellChange(input_path, output_path):
    df = pd.read_csv(input_path, header=None)
    df[['key', 'value']] = df[0].str.split('.', expand=True)
    df.to_csv(output_path, index=False, header=False)


def countCellDifference(clean_path, dirty_path):
    df_dirty = pd.read_csv(dirty_path, dtype=str)
    df_clean = pd.read_csv(clean_path, dtype=str)
    differences = df_dirty.ne(df_clean)
    print(differences.sum().sum())


def countTupleDifference(clean_path, dirty_path):
    df_dirty = pd.read_csv(dirty_path, dtype=str)
    df_clean = pd.read_csv(clean_path, dtype=str)
    differences = df_dirty.ne(df_clean).any(axis=1)
    print(differences.sum())


# indexData("tax_200k/tax_200k_clean.csv", "tax_200k/tax_200k_clean_id.csv")
# separateCellChange("tax_200k/dirty_mix_0.5/cellChanges.csv", "tax_200k/dirty_mix_0.5/cell_changes.csv")
countCellDifference("tax_200k/tax_200k_clean_id.csv", "tax_200k/dirty_mix_2/dirty_tax_null.csv")
countTupleDifference("tax_200k/tax_200k_clean_id.csv", "tax_200k/dirty_mix_2/dirty_tax_null.csv")
