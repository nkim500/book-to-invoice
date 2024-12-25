import streamlit as st

import utils
from config import AppConfig
from config import BusinessEntityParams


def initialize_state():
    st.set_page_config(layout="wide")
    if "statement_date" not in st.session_state:
        st.session_state["statement_date"] = None
    if "props" not in st.session_state:
        st.session_state.props = None
    if "prop" not in st.session_state:
        st.session_state.prop = None


app_config = AppConfig()

initialize_state()

try:
    st.session_state.props = utils.get_properties()
except FileNotFoundError:
    st.error("Property file not found")

utils.statement_date_widget()

utils.properties_widget(st.session_state.props)


def main():
    if "generate_invoices" not in st.session_state:
        st.session_state.generate_invoices = False
    if "download_triggered" not in st.session_state:
        st.session_state.download_triggered = False
    if "uploaded_water" not in st.session_state:
        st.session_state.uploaded_water = None
    if "uploaded_book" not in st.session_state:
        st.session_state.uploaded_book = False
    if "sheet_name" not in st.session_state:
        st.session_state.sheet_name = None
    if "sheet_name_correct" not in st.session_state:
        st.session_state.sheet_name_correct = False
    if "prop" not in st.session_state:
        st.session_state.prop = None
    if "override_water" not in st.session_state:
        st.session_state.override_water = False

    template_path = app_config.template_path
    export_path = app_config.output_path
    company = BusinessEntityParams()
    statement_date = st.session_state.statement_date

    st.header("Generate invoice from book")

    st.markdown("### Upload bookkeeping file")

    st.session_state.uploaded_book = st.file_uploader(
        "Upload the bookkeeping file (.xlsx)", type=["xlsx"]
    )
    st.session_state.sheet_name = st.text_input(
        "Enter the name of the bookkeeping worksheet to use for invoicing (Invoices will not be generated if sheet name is unspecified):",  # noqa: E501\
        value=None,
    )

    if st.session_state.uploaded_book:
        st.success("Bookkeeping file is uploaded")
        if st.session_state.sheet_name and len(st.session_state.sheet_name) >= 0:
            try:
                utils.ingest_bookkeeping_excel(
                    st.session_state.uploaded_book, sheet_name=st.session_state.sheet_name
                )
                st.session_state.sheet_name_correct = True
            except Exception as e:
                print(e)
                st.error(
                    f"Sheet name {st.session_state.sheet_name} does not exist. \
                    If sheet name is left blank, the last worksheet will be invoiced."
                )
    else:
        st.info("Bookkeeping file needs to be uploaded")

    st.markdown("### Upload water report")
    st.info("Note, current reading month is usually one month before the statement date")
    st.session_state.uploaded_water = st.file_uploader(
        "Upload the water report Excel file (.xlsx)", type=["xlsx"]
    )

    if st.session_state.uploaded_water:
        st.success("Water usage report uploaded")

    st.session_state.override_water = st.sidebar.checkbox(
        label="Check to skip water report upload",
    )

    water_check = st.session_state.uploaded_water or st.session_state.override_water

    st.session_state.generate_invoices = st.button("Generate invoices")
    # st.session_state.upload_invoice_to_db = st.checkbox("Update database", value=True)

    if (
        water_check
        and st.session_state.uploaded_book is not None
        and st.session_state.sheet_name is not None
        and st.session_state.prop
        and st.session_state.generate_invoices
    ):
        utils.clear_directory(export_path)

        try:
            file_paths = utils.generate_invoice_from_user_inputs(
                book=st.session_state.uploaded_book,
                waters=st.session_state.uploaded_water,
                statement_date=statement_date,
                prop=st.session_state.prop,
                template_path=template_path,
                export_path=export_path,
                sheet_name=st.session_state.sheet_name,
                company=company,
            )
            st.write(f"Generated {len(file_paths)} invoice(s)")
            utils.user_download_invoice_zip(export_path)
        except AssertionError:
            st.error("Please make sure the worksheet name is correct")
            st.stop()
        except Exception as e:
            st.error(e)
            st.write("Wunnuheyo")


if __name__ == "__main__":
    main()
