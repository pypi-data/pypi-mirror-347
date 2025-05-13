import asyncio
import tempfile

import anyio
import mcp.types as types
import pytest
import yaml
from mcp import ClientSession

from mcp_dbutils.base import ConnectionServer
from mcp_dbutils.log import create_logger

# 创建测试用的 logger
logger = create_logger("test-tools", True)  # debug=True 以显示所有日志

@pytest.mark.asyncio
async def test_list_tables_tool(postgres_db, sqlite_db, mcp_config):
    """Test the list_tables tool with both PostgreSQL and SQLite connections"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml') as tmp:
        yaml.dump(mcp_config, tmp)
        tmp.flush()
        server = ConnectionServer(config_path=tmp.name)

        # Create bidirectional streams
        client_to_server_send, client_to_server_recv = anyio.create_memory_object_stream[types.JSONRPCMessage | Exception](10)
        server_to_client_send, server_to_client_recv = anyio.create_memory_object_stream[types.JSONRPCMessage](10)

        # Start server in background
        server_task = asyncio.create_task(
            server.server.run(
                client_to_server_recv,
                server_to_client_send,
                server.server.create_initialization_options(),
                raise_exceptions=True
            )
        )

        try:
            # Initialize client session
            client = ClientSession(server_to_client_recv, client_to_server_send)
            async with client:
                await client.initialize()

                # List available tools
                response = await client.list_tools()
                tool_names = [tool.name for tool in response.tools]
                assert "dbutils-list-tables" in tool_names
                assert "dbutils-run-query" in tool_names

                # Test list_tables tool with PostgreSQL
                result = await client.call_tool("dbutils-list-tables", {"connection": "test_pg"})
                assert len(result.content) == 1
                assert result.content[0].type == "text"
                # 检查数据库类型前缀
                assert "[postgres]" in result.content[0].text
                assert "users" in result.content[0].text

                # Test list_tables tool with SQLite
                result = await client.call_tool("dbutils-list-tables", {"connection": "test_sqlite"})
                assert len(result.content) == 1
                assert result.content[0].type == "text"
                # 检查数据库类型前缀
                assert "[sqlite]" in result.content[0].text
                assert "products" in result.content[0].text

        finally:
            # Cleanup
            server_task.cancel()
            try:
                await server_task
            except asyncio.CancelledError:
                pass

            # Close streams
            await client_to_server_send.aclose()
            await client_to_server_recv.aclose()
            await server_to_client_send.aclose()
            await server_to_client_recv.aclose()

@pytest.mark.asyncio
async def test_describe_table_tool(postgres_db, sqlite_db, mcp_config):
    """Test the dbutils-describe-table tool with both PostgreSQL and SQLite connections"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml') as tmp:
        yaml.dump(mcp_config, tmp)
        tmp.flush()
        server = ConnectionServer(config_path=tmp.name)

        # Create bidirectional streams
        client_to_server_send, client_to_server_recv = anyio.create_memory_object_stream[types.JSONRPCMessage | Exception](10)
        server_to_client_send, server_to_client_recv = anyio.create_memory_object_stream[types.JSONRPCMessage](10)

        # Start server in background
        server_task = asyncio.create_task(
            server.server.run(
                client_to_server_recv,
                server_to_client_send,
                server.server.create_initialization_options(),
                raise_exceptions=True
            )
        )

        try:
            # Initialize client session
            client = ClientSession(server_to_client_recv, client_to_server_send)
            async with client:
                await client.initialize()

                # Verify tool is available
                response = await client.list_tools()
                tool_names = [tool.name for tool in response.tools]
                assert "dbutils-describe-table" in tool_names

                # Test PostgreSQL describe-table
                pg_args = {"connection": "test_pg", "table": "users"}
                result = await client.call_tool("dbutils-describe-table", pg_args)
                assert len(result.content) == 1
                assert result.content[0].type == "text"
                assert "[postgres]" in result.content[0].text
                assert "Table: users" in result.content[0].text
                assert "Columns:" in result.content[0].text

                # Test SQLite describe-table
                sqlite_args = {"connection": "test_sqlite", "table": "products"}
                result = await client.call_tool("dbutils-describe-table", sqlite_args)
                assert len(result.content) == 1
                assert result.content[0].type == "text"
                assert "[sqlite]" in result.content[0].text
                assert "Table: products" in result.content[0].text
                assert "Columns:" in result.content[0].text

        finally:
            # Cleanup
            server_task.cancel()
            try:
                await server_task
            except asyncio.CancelledError:
                pass

            # Close streams
            await client_to_server_send.aclose()
            await client_to_server_recv.aclose()
            await server_to_client_send.aclose()
            await server_to_client_recv.aclose()

@pytest.mark.asyncio
async def test_get_ddl_tool(postgres_db, sqlite_db, mcp_config):
    """Test the dbutils-get-ddl tool with both PostgreSQL and SQLite connections"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml') as tmp:
        yaml.dump(mcp_config, tmp)
        tmp.flush()
        server = ConnectionServer(config_path=tmp.name)

        # Create bidirectional streams
        client_to_server_send, client_to_server_recv = anyio.create_memory_object_stream[types.JSONRPCMessage | Exception](10)
        server_to_client_send, server_to_client_recv = anyio.create_memory_object_stream[types.JSONRPCMessage](10)

        # Start server in background
        server_task = asyncio.create_task(
            server.server.run(
                client_to_server_recv,
                server_to_client_send,
                server.server.create_initialization_options(),
                raise_exceptions=True
            )
        )

        try:
            # Initialize client session
            client = ClientSession(server_to_client_recv, client_to_server_send)
            async with client:
                await client.initialize()

                # Verify tool is available
                response = await client.list_tools()
                tool_names = [tool.name for tool in response.tools]
                assert "dbutils-get-ddl" in tool_names

                # Test PostgreSQL get-ddl
                pg_args = {"connection": "test_pg", "table": "users"}
                result = await client.call_tool("dbutils-get-ddl", pg_args)
                assert len(result.content) == 1
                assert result.content[0].type == "text"
                assert "[postgres]" in result.content[0].text
                assert "CREATE TABLE users" in result.content[0].text

                # Test SQLite get-ddl
                sqlite_args = {"connection": "test_sqlite", "table": "products"}
                result = await client.call_tool("dbutils-get-ddl", sqlite_args)
                assert len(result.content) == 1
                assert result.content[0].type == "text"
                assert "[sqlite]" in result.content[0].text
                assert "CREATE TABLE products" in result.content[0].text

        finally:
            # Cleanup
            server_task.cancel()
            try:
                await server_task
            except asyncio.CancelledError:
                pass

            # Close streams
            await client_to_server_send.aclose()
            await client_to_server_recv.aclose()
            await server_to_client_send.aclose()
            await server_to_client_recv.aclose()

@pytest.mark.asyncio
async def test_list_indexes_tool(postgres_db, sqlite_db, mcp_config):
    """Test the dbutils-list-indexes tool with both PostgreSQL and SQLite connections"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml') as tmp:
        yaml.dump(mcp_config, tmp)
        tmp.flush()
        server = ConnectionServer(config_path=tmp.name)

        # Create bidirectional streams
        client_to_server_send, client_to_server_recv = anyio.create_memory_object_stream[types.JSONRPCMessage | Exception](10)
        server_to_client_send, server_to_client_recv = anyio.create_memory_object_stream[types.JSONRPCMessage](10)

        # Start server in background
        server_task = asyncio.create_task(
            server.server.run(
                client_to_server_recv,
                server_to_client_send,
                server.server.create_initialization_options(),
                raise_exceptions=True
            )
        )

        try:
            # Initialize client session
            client = ClientSession(server_to_client_recv, client_to_server_send)
            async with client:
                await client.initialize()

                # Verify tool is available
                response = await client.list_tools()
                tool_names = [tool.name for tool in response.tools]
                assert "dbutils-list-indexes" in tool_names

                # Test PostgreSQL list-indexes
                pg_args = {"connection": "test_pg", "table": "users"}
                result = await client.call_tool("dbutils-list-indexes", pg_args)
                assert len(result.content) == 1
                assert result.content[0].type == "text"
                assert "[postgres]" in result.content[0].text

                # Test SQLite list-indexes
                sqlite_args = {"connection": "test_sqlite", "table": "products"}
                result = await client.call_tool("dbutils-list-indexes", sqlite_args)
                assert len(result.content) == 1
                assert result.content[0].type == "text"
                assert "[sqlite]" in result.content[0].text

        finally:
            # Cleanup
            server_task.cancel()
            try:
                await server_task
            except asyncio.CancelledError:
                pass

            # Close streams
            await client_to_server_send.aclose()
            await client_to_server_recv.aclose()
            await server_to_client_send.aclose()
            await server_to_client_recv.aclose()

@pytest.mark.asyncio
async def test_list_tables_tool_errors(postgres_db, mcp_config):
    """Test error cases for list_tables tool"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml') as tmp:
        # 写入有效的配置
        yaml.dump(mcp_config, tmp)
        tmp.flush()
        server = ConnectionServer(config_path=tmp.name)

        # 创建双向流
        client_to_server_send, client_to_server_recv = anyio.create_memory_object_stream[types.JSONRPCMessage | Exception](10)
        server_to_client_send, server_to_client_recv = anyio.create_memory_object_stream[types.JSONRPCMessage](10)

        # 在后台启动服务器
        server_task = asyncio.create_task(
            server.server.run(
                client_to_server_recv,
                server_to_client_send,
                server.server.create_initialization_options(),
                raise_exceptions=False  # 不抛出异常，让客户端接收错误响应
            )
        )

        try:
            # 初始化客户端会话
            client = ClientSession(server_to_client_recv, client_to_server_send)
            async with client:
                await client.initialize()

                # 测试场景1：不存在的连接名
                result = await client.call_tool("dbutils-list-tables", {"connection": "non_existent_connection"})
                print(f"收到响应: {result}")
                assert result.isError, "应该返回错误状态"
                assert len(result.content) == 1
                assert result.content[0].type == "text"
                assert "Connection not found" in result.content[0].text
                assert "non_existent_connection" in result.content[0].text

                # 测试场景2：缺少必需的连接参数
                result = await client.call_tool("dbutils-list-tables", {})
                print(f"收到响应: {result}")
                assert result.isError, "应该返回错误状态"
                assert len(result.content) == 1
                assert result.content[0].type == "text"
                assert "Connection name must be specified" in result.content[0].text

        finally:
            # 清理
            server_task.cancel()
            try:
                await server_task
            except asyncio.CancelledError:
                pass

            # 关闭流
            await client_to_server_send.aclose()
            await client_to_server_recv.aclose()
            await server_to_client_send.aclose()
            await server_to_client_recv.aclose()
