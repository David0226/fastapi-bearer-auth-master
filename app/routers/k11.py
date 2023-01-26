from fastapi import APIRouter
from def_custom.dbconn import influxdb_conn
from database import k11_sql

router = APIRouter(
    prefix="/k11",
    tags=["k11"],
    responses={404: {"description":"Not Found"}}
)


@router.get("/")
async def read_root():
    return {"Hello": "World"}


@router.get("/read_racks")
async def read_racks():
    return k11_sql.read_racks()


@router.get("/read_racks_as_csv")
async def read_racks_as_csv():
    return k11_sql.read_racks_as_csv()


@router.get("/read_racks_as_df")
def test4():
    return k11_sql.read_racks_as_df()


@router.get("/read_racks_mean_as_csv")
def test4():
    return k11_sql.read_racks_mean_as_csv()


@router.get("/read_as_table")
def read_as_table():
    return k11_sql.read_root_as_table()


@router.get("/read_cell_as_table")
def read_cell_as_table():
    return k11_sql.read_cell_as_table()


@router.get("/read_cell")
def read_cell():
    return k11_sql.read_cell()


@router.get("/read_bank_summary")
def read_bank_summary():
    return k11_sql.read_bank_summary()


@router.get("/read_bank_summary_cur")
def read_bank_summary_cur():
    return k11_sql.read_bank_summary_cur()


@router.get("/read_bank_summary_soc")
def read_bank_summary_soc():
    return k11_sql.read_bank_summary_soc()


@router.get("/read_cells_for_histogram/{bank_idx}")
def read_cells_for_histogram(bank_idx: int = 0):
    return k11_sql.read_cells_for_histogram(bank_idx)



# 20220420 hjh added start
@router.get("/read_rack_status/{bank_idx}/{rack_idx}")
def read_rack_status(bank_idx: int, rack_idx: int):
    return k11_sql.read_rack_status(bank_idx, rack_idx)

@router.get("/read_module_status/{bank_idx}/{rack_idx}")
def read_module_status(bank_idx: int, rack_idx: int):
    return k11_sql.read_module_status(bank_idx, rack_idx)

@router.get("/read_cell_status/{bank_idx}/{rack_idx}/{val_type}")
def read_cell_status(bank_idx: int, rack_idx: int, val_type: str):
    return k11_sql.read_cell_status(bank_idx, rack_idx, val_type)
# hjh added end
