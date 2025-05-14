from grapheteria import WorkflowEngine
from fastapi import APIRouter, HTTPException, Body
from typing import Dict, Any, List, Optional
from grapheteria.composio import ToolManager
from grapheteria.utils import FileSystemStorage

router = APIRouter()


@router.get("/workflows/create/{workflow_id}")
async def create_workflow(workflow_id: str):
    try:
        workflow = WorkflowEngine(workflow_id=workflow_id)

        run_id = workflow.run_id

        return {
            "message": "Workflow created",
            "run_id": run_id,
            "execution_data": workflow.tracking_data,
        }
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=500, detail=f"Failed to start workflow: {str(e)}"
        )


@router.post("/workflows/step/{workflow_id}/{run_id}")
async def step_workflow(
    workflow_id: str,
    run_id: str,
    input_data: Optional[Dict[str, Any]] = Body(None),
    resume_from: Optional[int] = Body(None),
    fork: bool = Body(False),
):
    # Create new workflow with specified parameters
    workflow = WorkflowEngine(
        workflow_id=workflow_id, run_id=run_id, resume_from=resume_from, fork=fork
    )

    try:
        await workflow.step(input_data=input_data)
    except Exception:
        # Just catch the exception, don't return here
        pass

    # Return response regardless of whether an exception occurred
    return {"message": "Workflow stepped", "execution_data": workflow.tracking_data}


@router.post("/workflows/run/{workflow_id}/{run_id}")
async def run_workflow(
    workflow_id: str,
    run_id: str,
    input_data: Optional[Dict[str, Any]] = Body(None),
    resume_from: Optional[int] = Body(None),
    fork: bool = Body(False),
):
    # Create new workflow with specified parameters
    workflow = WorkflowEngine(
        workflow_id=workflow_id, run_id=run_id, resume_from=resume_from, fork=fork
    )

    try:
        await workflow.run(input_data=input_data)
    except Exception:
        # Just catch the exception, don't return here
        pass

    return {"message": "Workflow run", "execution_data": workflow.tracking_data}

@router.get("/logs")
async def get_logs():
    return FileSystemStorage().list_workflows()


@router.get("/logs/{workflow_id}")
async def get_workflow_logs(workflow_id: str):
    return FileSystemStorage().list_runs(workflow_id)


@router.get("/logs/{workflow_id}/{run_id}")
async def get_run_logs(workflow_id: str, run_id: str):
    return FileSystemStorage().load_state(workflow_id, run_id)


@router.get("/authenticate/{tool_name}")
async def authenticate_tool(tool_name: str):
    tool_manager = ToolManager()
    return tool_manager.authenticate_tool(tool_name)


@router.post("/workflows/update/{workflow_id}")
async def update_workflow(
    workflow_id: str, 
    data: Dict[str, Any] = Body(...)
):
    try:
        # Extract parameters from the request body
        update_prompt = data.get("update_prompt")
        selected_integrations = data.get("selected_integrations", [])
        print(update_prompt, selected_integrations)
        
        # Validate required parameters
        if not update_prompt:
            return {"message": "Enter a prompt to update the workflow"}
            
        # Create tool manager if integrations are selected
        tool_manager = ToolManager() if selected_integrations not in [None, []] else None
        
        # Update the workflow
        _ = WorkflowEngine.update_workflow(
            workflow_id=workflow_id,
            update_description=update_prompt,
            tools=selected_integrations,
            tool_manager=tool_manager
        )
        
        return {"message": "I have successfully updated the workflow!"}
    except Exception as e:
        print(f"Error updating workflow: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to update workflow: {str(e)}"
        )

