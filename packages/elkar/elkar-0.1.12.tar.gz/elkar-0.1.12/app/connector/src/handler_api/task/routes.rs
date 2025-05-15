use axum::{Json, extract::Path};
use database_schema::enum_definitions::task::TaskType;
use http::StatusCode;
use utoipa_axum::{router::OpenApiRouter, routes};

use crate::{
    extensions::{
        errors::{AppResult, ServiceError},
        extractors::{api_key_context::ApiKeyContext, query_params::Qs},
    },
    service::task::{
        create_a2a::{CreateTaskA2AParams, create_task_a2a},
        retrieve_a2a::{RetrieveTaskA2AParams, retrieve_task_a2a},
        update::{UpdateTaskParams, update_task},
        upsert_a2a_client::{CreateTaskA2AClientParams, create_task_a2a_client},
    },
};

use super::schemas::{
    CreateTaskInput, GetTaskQueryParams, TaskResponse, UpdateTaskInput, UpsertTaskA2AInput,
};

pub fn task_api_router() -> OpenApiRouter {
    OpenApiRouter::new()
        .routes(routes!(ep_upsert_task))
        .routes(routes!(ep_get_task))
        .routes(routes!(ep_update_task))
        .routes(routes!(ep_upsert_task_client_side))
        .routes(routes!(ep_get_task_client_side))
}

#[utoipa::path(
    post,
    path = "/tasks",
    tag = "task",
    summary = "Create a task",
    responses(
        (status = 200, body = TaskResponse)
    )
)]
pub async fn ep_upsert_task(
    context: ApiKeyContext,
    Json(create_task_input): Json<CreateTaskInput>,
) -> AppResult<Json<TaskResponse>> {
    let Some(agent_id) = context.agent_id else {
        return Err(ServiceError::new()
            .status_code(StatusCode::UNAUTHORIZED)
            .error_type("Agent ID is required")
            .into());
    };
    let mut conn = context.async_pool.get().await?;
    let params = CreateTaskA2AParams {
        send_task_params: create_task_input.send_task_params,
        agent_id,
        counterparty_identifier: create_task_input.counterparty_identifier,
        task_type: create_task_input.task_type,
    };
    let task = create_task_a2a(params, &mut conn).await?;
    Ok(Json(task.into()))
}

#[utoipa::path(
    get,
    path = "/tasks/{task_id}",
    tag = "task",
    summary = "Get a task from the server side",
    params(
        ("task_id" = String, Path, description = "The ID of the task to get"),
        ("caller_id" = Option<String>, Query, description = "The ID of the caller"),
        ("history_length" = Option<u32>, Query, description = "The number of history messages to return")
    ),
    responses(
        (status = 200, body = TaskResponse)
    )
)]
pub async fn ep_get_task(
    context: ApiKeyContext,
    Path(task_id): Path<String>,
    Qs(query_params): Qs<GetTaskQueryParams>,
) -> AppResult<Json<TaskResponse>> {
    let Some(agent_id) = context.agent_id else {
        return Err(ServiceError::new()
            .status_code(StatusCode::UNAUTHORIZED)
            .error_type("Agent ID is required")
            .into());
    };
    let params = RetrieveTaskA2AParams {
        task_id,
        agent_id,
        caller_id: query_params.caller_id,
        task_type: TaskType::Incoming,
    };
    let mut conn = context.async_pool.get().await?;
    let task = retrieve_task_a2a(params, &mut conn).await?;
    Ok(Json(task.into()))
}

#[utoipa::path(
    get,
    path = "/client-side/tasks/{task_id}",
    tag = "task",
    summary = "Get a task from the client side",
    params(
        ("task_id" = String, Path, description = "The ID of the task to get"),
        ("caller_id" = Option<String>, Query, description = "The ID of the caller"),
        ("history_length" = Option<u32>, Query, description = "The number of history messages to return")
    ),
    responses(
        (status = 200, body = TaskResponse)
    )
)]
pub async fn ep_get_task_client_side(
    context: ApiKeyContext,
    Path(task_id): Path<String>,
    Qs(query_params): Qs<GetTaskQueryParams>,
) -> AppResult<Json<TaskResponse>> {
    let Some(agent_id) = context.agent_id else {
        return Err(ServiceError::new()
            .status_code(StatusCode::UNAUTHORIZED)
            .error_type("Agent ID is required")
            .into());
    };
    let params = RetrieveTaskA2AParams {
        task_id,
        agent_id,
        caller_id: query_params.caller_id,
        task_type: TaskType::Outgoing,
    };
    let mut conn = context.async_pool.get().await?;
    let task = retrieve_task_a2a(params, &mut conn).await?;
    Ok(Json(task.into()))
}

#[utoipa::path(
    put,
    path = "/tasks/{task_id}",
    tag = "task",
    summary = "Update a task",    
    responses(
        (status = 200, body = TaskResponse)
    )
)]
pub async fn ep_update_task(
    context: ApiKeyContext,
    Path(task_id): Path<String>,
    Json(update_task_input): Json<UpdateTaskInput>,
) -> AppResult<Json<TaskResponse>> {
    let Some(agent_id) = context.agent_id else {
        return Err(ServiceError::new()
            .status_code(StatusCode::UNAUTHORIZED)
            .error_type("Agent ID is required")
            .into());
    };
    let mut conn = context.async_pool.get().await?;
    let params = UpdateTaskParams {
        status: update_task_input.status,
        artifacts_updates: update_task_input.artifacts_updates,
        new_messages: update_task_input.new_messages,
        push_notification: update_task_input.push_notification,
        caller_id: update_task_input.caller_id,
    };
    let task = update_task(agent_id, task_id, params, &mut conn).await?;
    Ok(Json(task.into()))
}

#[utoipa::path(
    post,
    path = "/client-side/tasks",
    tag = "task",
    summary = "Upsert a task",
    responses(
        (status = 200, body = TaskResponse)
    )
)]
pub async fn ep_upsert_task_client_side(
    context: ApiKeyContext,
    Json(create_task_input): Json<UpsertTaskA2AInput>,
) -> AppResult<Json<TaskResponse>> {
    let mut conn = context.async_pool.get().await?;
    let params = CreateTaskA2AClientParams {
        task: create_task_input.task,
        agent_id: context.agent_id.unwrap(),
        counterparty_identifier: create_task_input.counterparty_identifier,
        server_agent_url: create_task_input.server_agent_url,
    };
    let task = create_task_a2a_client(params, &mut conn).await?;
    Ok(Json(task.into()))
}
