from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.exceptions import HTTPException

from api_models import QueryRequest, QueryResponse, InsertProposalRequest, InsertProposalResponse, \
    InsertApprovalResponse, InsertApprovalRequest
from database_config import get_db
from db_agent import query_db_with_natural_language, propose_insert, approve_and_execute

router = APIRouter(prefix="/agent", tags=["DB Agent"])

@router.post(path="/", response_model=QueryResponse)
def query_db(request: QueryRequest) -> QueryResponse:
    try:
        thread_id = request.thread_id or "1"
        result = query_db_with_natural_language(request.query, thread_id=thread_id)
        return QueryResponse(query=request.query, result=result, thread_id=thread_id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=str(e))

@router.post("/insert/propose", response_model=InsertProposalResponse)
async def propose_insert_request(request: InsertProposalRequest, session: AsyncSession = Depends(get_db)) -> InsertProposalResponse:
    try:
        proposal = await propose_insert(request.query, session=session)
        return InsertProposalResponse(
            approval_id=proposal["approval_id"],
            sql=proposal["sql"],
            status="pending"
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.post("/insert/approve", response_model=InsertApprovalResponse)
async def approve_proposal(request: InsertApprovalRequest, session: AsyncSession = Depends(get_db)):
    try:
        result = await approve_and_execute(approval_id=request.approval_id,
                                           approve=request.approve,
                                           session=session)

        status_val = "approved" if request.approve else "rejected"
        return InsertApprovalResponse(
            approval_id=request.approval_id,
            status=status_val,
            result=result
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


