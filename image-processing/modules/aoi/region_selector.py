from .province_selector import load_admin_data


def normalize_admin_code(code):
    code = str(code).strip()

    if not code or code.lower() == "nan":
        return ""

    parts = code.split(".")

    if len(parts) == 2:
        province = parts[0].zfill(2)
        region = parts[1]

        if len(region) == 1:
            region += "0"

        return f"{province}.{region}"

    return code


def get_regions(province, region_type=None):

    data = load_admin_data()

    selected = data[
        data["WADMPR"].str.casefold()
        == province.strip().casefold()
    ].copy()

    if region_type:
        region_type = region_type.lower()

        if region_type == "kabupaten":
            selected = selected[selected["TIPADM"] == "4"]

        elif region_type == "kota":
            selected = selected[selected["TIPADM"] == "5"]

        else:
            raise ValueError(
                "Tipe wilayah harus kabupaten atau kota."
            )

    selected["KDPKAB"] = selected["KDPKAB"].apply(
        normalize_admin_code
    )

    selected = selected[
        selected["KDPKAB"] != ""
    ].drop_duplicates(
        subset=["KDPKAB"],
        keep="first"
    )

    selected = selected.sort_values("NAMOBJ")

    return [
        {
            "name": row["NAMOBJ"],
            "code": row["KDPKAB"],
            "province": row["WADMPR"],
            "type": (
                "Kota" if row["TIPADM"] == "5"
                else "Kabupaten"
            )
        }
        for _, row in selected.iterrows()
    ]


if __name__ == "__main__":

    province = "Sulawesi Tenggara"

    print("===== RIMBARA REGION SELECTOR =====")
    print("Provinsi:", province)

    regions = get_regions(province)

    print("Total wilayah:", len(regions))

    for region in regions:
        print(
            f'{region["code"]} | '
            f'{region["type"]} | '
            f'{region["name"]}'
        )
