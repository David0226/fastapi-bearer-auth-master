from fastapi import APIRouter
from def_custom.dbconn import influxdb_conn


router = APIRouter(
    prefix="/k11",
    tags=["k11"],
    responses={"404",{"description":"Not Found"}}
)



@router.get("/")
def read_root():
    return {"Hello": "World"}


@router.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}



@router.get("/test2")
def test2(request: Request):
    return k11.read_racks()


@router.get("/read_racks_as_csv")
def test3(request: Request):
    return k11.read_racks_as_csv()


@router.get("/test4")
def test4(request: Request):
    return k11.read_racks_as_df()


@router.get("/test5")
def test4(request: Request):
    return k11.read_racks_mean_as_csv()


@router.get("/read_as_table")
def read_as_table(request: Request):
    return k11.read_root_as_table()


@router.get("/read_cell_as_table")
def read_cell_as_table(request: Request):
    return k11.read_cell_as_table()


@router.get("/read_cell")
def read_cell(request: Request):
    return k11.read_cell()


@router.get("/read_bank_summary")
def read_bank_summary(request: Request):
    return k11.read_bank_summary()


@router.get("/read_bank_summary_cur")
def read_bank_summary_cur(request: Request):
    return k11.read_bank_summary_cur()


@router.get("/read_bank_summary_soc")
def read_bank_summary_soc(request: Request):
    return k11.read_bank_summary_soc()


@router.get("/read_cells_for_histogram/{bank_idx}")
def read_cells_for_histogram(request: Request, bank_idx: int = 0):
    return k11.read_cells_for_histogram(bank_idx)



# 20220420 hjh added start
@router.get("/read_rack_status/{bank_idx}/{rack_idx}")
def read_rack_status(request: Request, bank_idx: int, rack_idx: int):
    return k11.read_rack_status(bank_idx, rack_idx)

@router.get("/read_module_status/{bank_idx}/{rack_idx}")
def read_module_status(request: Request, bank_idx: int, rack_idx: int):
    return k11.read_module_status(bank_idx, rack_idx)

@router.get("/read_cell_status/{bank_idx}/{rack_idx}/{val_type}")
def read_cell_status(request: Request, bank_idx: int, rack_idx: int, val_type: str):
    return k11.read_cell_status(bank_idx, rack_idx, val_type)
# hjh added end
