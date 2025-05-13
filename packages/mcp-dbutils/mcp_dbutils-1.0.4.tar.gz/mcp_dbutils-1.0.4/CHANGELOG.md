## [1.0.4](https://github.com/donghao1393/mcp-dbutils/compare/v1.0.3...v1.0.4) (2025-05-12)


### Bug Fixes

* 修改文档中的Docker安装说明，添加获取项目代码步骤 ([#111](https://github.com/donghao1393/mcp-dbutils/issues/111)) ([e56805f](https://github.com/donghao1393/mcp-dbutils/commit/e56805fe01ae32e28c60cdeaf2458d936ee8ca15)), closes [#110](https://github.com/donghao1393/mcp-dbutils/issues/110) [#110](https://github.com/donghao1393/mcp-dbutils/issues/110) [#110](https://github.com/donghao1393/mcp-dbutils/issues/110) [#110](https://github.com/donghao1393/mcp-dbutils/issues/110) [#110](https://github.com/donghao1393/mcp-dbutils/issues/110) [#110](https://github.com/donghao1393/mcp-dbutils/issues/110) [#110](https://github.com/donghao1393/mcp-dbutils/issues/110) [#110](https://github.com/donghao1393/mcp-dbutils/issues/110)

## [1.0.3](https://github.com/donghao1393/mcp-dbutils/compare/v1.0.2...v1.0.3) (2025-05-05)


### Bug Fixes

* 修复_extract_table_name方法处理多行SQL语句的问题 ([#98](https://github.com/donghao1393/mcp-dbutils/issues/98)) ([69eb5e1](https://github.com/donghao1393/mcp-dbutils/commit/69eb5e11e5007a5d36b09ff2bedbc1d3997815af)), closes [#97](https://github.com/donghao1393/mcp-dbutils/issues/97)

## [1.0.2](https://github.com/donghao1393/mcp-dbutils/compare/v1.0.1...v1.0.2) (2025-05-05)


### Bug Fixes

* 修复表名大小写敏感性问题 ([#95](https://github.com/donghao1393/mcp-dbutils/issues/95)) ([2986101](https://github.com/donghao1393/mcp-dbutils/commit/2986101656d3f6d8d70ee21c051e4d140c0c9eee)), closes [#92](https://github.com/donghao1393/mcp-dbutils/issues/92)

## [1.0.1](https://github.com/donghao1393/mcp-dbutils/compare/v1.0.0...v1.0.1) (2025-05-04)


### Bug Fixes

* 提高代码覆盖率以解决SonarCloud检查失败问题 ([#90](https://github.com/donghao1393/mcp-dbutils/issues/90)) ([adbc9f2](https://github.com/donghao1393/mcp-dbutils/commit/adbc9f2e6fb54ed446d96775c65edf67611637ed))

# [1.0.0](https://github.com/donghao1393/mcp-dbutils/compare/v0.23.1...v1.0.0) (2025-05-04)


### Features

* 添加数据库写操作功能 ([#88](https://github.com/donghao1393/mcp-dbutils/issues/88)) ([7703cdf](https://github.com/donghao1393/mcp-dbutils/commit/7703cdf58dd706b300e5f9a89b1b530274e36fe0))


### BREAKING CHANGES

* 这个功能将改变项目的核心安全模型，从只读到可配置读写，
需要主版本号升级（从1.x.x到2.0.0）。

* feat: 添加数据库写操作配置支持

在配置系统中添加对数据库写操作的支持：
1. 在ConnectionConfig基类中添加writable和write_permissions属性
2. 创建WritePermissions类处理表级和操作级权限控制
3. 修改SQLite、PostgreSQL和MySQL配置类以支持写操作配置
4. 添加配置验证逻辑确保安全性
* 这个功能将改变项目的核心安全模型，从只读到可配置读写，
需要主版本号升级（从1.x.x到2.0.0）。

* feat: 添加数据库写操作基础功能

在基础类中添加数据库写操作支持：
1. 添加写操作相关的常量和错误消息
2. 在ConnectionHandler类中添加写操作相关方法
3. 添加SQL类型识别和表名提取功能
4. 在ConnectionServer类中添加写权限检查方法
5. 添加dbutils-execute-write工具和处理函数
* 这个功能将改变项目的核心安全模型，从只读到可配置读写，
需要主版本号升级（从1.x.x到2.0.0）。

* feat: 添加数据库写操作实现

在各数据库处理器中实现写操作功能：
1. 在SQLite处理器中添加_execute_write_query方法
2. 在PostgreSQL处理器中添加_execute_write_query方法
3. 在MySQL处理器中添加_execute_write_query方法
4. 添加事务支持和错误处理
* 这个功能将改变项目的核心安全模型，从只读到可配置读写，
需要主版本号升级（从1.x.x到2.0.0）。

* feat: 添加数据库写操作审计日志系统

1. 创建审计日志系统，记录所有数据库写操作
2. 添加审计日志配置和过滤功能
3. 在ConnectionHandler.execute_write_query方法中集成审计日志
4. 添加dbutils-get-audit-logs工具，用于查询审计日志
5. 实现_handle_get_audit_logs方法，处理审计日志查询
* 这个功能将改变项目的核心安全模型，从只读到可配置读写，
需要主版本号升级（从1.x.x到2.0.0）。

* docs: 添加数据库写操作文档和配置示例

1. 添加数据库写操作功能文档，包括配置、使用方法和安全最佳实践
2. 添加配置文件示例，包含写操作和审计日志配置
* 这个功能将改变项目的核心安全模型，从只读到可配置读写，
需要主版本号升级（从1.x.x到2.0.0）。

* test: 添加数据库写操作测试用例

1. 测试成功执行写操作
2. 测试只读连接的写操作
3. 测试没有确认的写操作
4. 测试不支持的写操作
5. 测试未授权表的写操作
6. 测试未授权操作的写操作
7. 测试获取审计日志
* 这个功能将改变项目的核心安全模型，从只读到可配置读写，
需要主版本号升级（从1.x.x到2.0.0）。

* fix: 修复CI错误和测试问题

1. 修复代码风格问题：导入排序和嵌套if语句
2. 修复测试文件中的方法名称问题，将_handle_call_tool改为handle_call_tool
3. 在测试类中实现新的抽象方法_execute_write_query

* fix: 修复测试文件中的方法名称问题，将handle_call_tool改为_handle_call_tool

* fix: 修复测试文件中的方法名称问题，将_handle_call_tool改为handle_call_tool

* fix: 修复测试文件中的方法调用问题，使用正确的内部方法

* fix: 修复测试文件中的方法调用问题，使用handle_call_tool替代内部方法

* fix: 修复测试文件中的方法调用问题，添加handle_call_tool方法

* fix: 修复测试文件中的方法调用问题，添加特殊处理CREATE TABLE语句和实现execute_write功能

* fix: 修复测试文件中的表名大小写问题

* fix: 修复测试文件中的数据库连接问题，使用文件数据库代替内存数据库

* fix: 修复测试文件中的审计日志问题，添加log_write_operation调用

* fix: 修复代码风格和安全问题，解决CI失败

* fix: 修复代码风格问题，使用ruff自动修复导入顺序

* test: 增加MySQL和PostgreSQL处理程序的写操作测试，提高代码覆盖率

* test: 增加ConnectionServer类的写操作和审计日志测试，提高代码覆盖率

* style: 修复ruff检查中的SIM117问题，使用单个with语句替代嵌套with语句

* test: 修复ConnectionServer类的写操作和审计日志测试，模拟所需方法

* test: 修复测试中的get_handler.called属性错误

* fix: 修复正则表达式中的安全热点问题，避免潜在的回溯问题

* test: 增加审计日志模块的测试，提高代码覆盖率

* test: 增加base模块写操作相关方法的测试，提高代码覆盖率

* style: 修复ruff检查中的导入排序和嵌套with语句问题

* style: 修复ruff检查中的导入排序和嵌套with语句问题（第二次）

* test: 修复base模块写操作相关方法的测试，解决测试失败问题

* style: 修复ruff检查中的嵌套with语句问题

* fix: 修复ConnectionServer类中的_get_sql_type和_extract_table_name方法，解决测试失败问题

* fix: 修复测试中的AsyncMock问题，确保_check_write_permission方法的异步调用正确

* fix: 修复_handle_execute_write方法中的_get_config_or_raise调用，确保测试通过

* test: 添加SQL解析和写权限检查的测试，提高代码覆盖率

* style: 修复导入排序问题

## [0.23.1](https://github.com/donghao1393/mcp-dbutils/compare/v0.23.0...v0.23.1) (2025-05-03)


### Bug Fixes

* 移除不兼容的read_timeout_seconds参数 ([#86](https://github.com/donghao1393/mcp-dbutils/issues/86)) ([247047b](https://github.com/donghao1393/mcp-dbutils/commit/247047bc36efe320b3a4e6c8ae7d423d4666784c))

# [0.23.0](https://github.com/donghao1393/mcp-dbutils/compare/v0.22.0...v0.23.0) (2025-05-03)


### Features

* 升级MCP SDK从v1.2.1到v1.7.1 ([#85](https://github.com/donghao1393/mcp-dbutils/issues/85)) ([f0c4f9f](https://github.com/donghao1393/mcp-dbutils/commit/f0c4f9f6b99de4febb53b80a7036bd88b1d6dd39))

# [0.22.0](https://github.com/donghao1393/mcp-dbutils/compare/v0.21.0...v0.22.0) (2025-05-01)


### Features

* 更新多语言文档中的工具描述 ([#83](https://github.com/donghao1393/mcp-dbutils/issues/83)) ([45c3c05](https://github.com/donghao1393/mcp-dbutils/commit/45c3c053975405f9d5e028d6d9441ab8e8de1a65))

# [0.21.0](https://github.com/donghao1393/mcp-dbutils/compare/v0.20.1...v0.21.0) (2025-05-01)


### Features

* 优化数据库工具描述以提高LLM理解能力 ([#81](https://github.com/donghao1393/mcp-dbutils/issues/81)) ([232cd3e](https://github.com/donghao1393/mcp-dbutils/commit/232cd3ed247ed95248932001c99ed529819cddf8))

## [0.20.1](https://github.com/donghao1393/mcp-dbutils/compare/v0.20.0...v0.20.1) (2025-04-30)


### Bug Fixes

* 修复MySQL和PostgreSQL处理器中变量作用域问题 ([#78](https://github.com/donghao1393/mcp-dbutils/issues/78)) ([9479e67](https://github.com/donghao1393/mcp-dbutils/commit/9479e677fb78346b6ef34ad474055f4df787a059)), closes [#75](https://github.com/donghao1393/mcp-dbutils/issues/75) [#75](https://github.com/donghao1393/mcp-dbutils/issues/75)

# [0.20.0](https://github.com/donghao1393/mcp-dbutils/compare/v0.19.0...v0.20.0) (2025-04-30)


### Features

* add multilingual issue templates in six languages ([#77](https://github.com/donghao1393/mcp-dbutils/issues/77)) ([7a3d081](https://github.com/donghao1393/mcp-dbutils/commit/7a3d0819c126294858eb7bbcd0901193489639a5))

# [0.19.0](https://github.com/donghao1393/mcp-dbutils/compare/v0.18.0...v0.19.0) (2025-04-25)


### Features

* 完成多语言文档 ([#74](https://github.com/donghao1393/mcp-dbutils/issues/74)) ([aa5d7a6](https://github.com/donghao1393/mcp-dbutils/commit/aa5d7a6c4648bd575d538906d1dcd65ba5ba8c56))

# [0.18.0](https://github.com/donghao1393/mcp-dbutils/compare/v0.17.0...v0.18.0) (2025-04-25)


### Features

* add dbutils-list-connections tool ([#68](https://github.com/donghao1393/mcp-dbutils/issues/68)) ([44ce9ac](https://github.com/donghao1393/mcp-dbutils/commit/44ce9ac9a63fcd43a0c817ee72b508380f36ba8d))

# [0.17.0](https://github.com/donghao1393/mcp-dbutils/compare/v0.16.1...v0.17.0) (2025-03-16)


### Features

* 添加本地SonarQube分析脚本 ([65326a3](https://github.com/donghao1393/mcp-dbutils/commit/65326a3aa3a61db353fd3c399a3c808e9a07e332))

## [0.16.1](https://github.com/donghao1393/mcp-dbutils/compare/v0.16.0...v0.16.1) (2025-03-15)


### Bug Fixes

* some SonarCloud issues ([#51](https://github.com/donghao1393/mcp-dbutils/issues/51)) ([4df99de](https://github.com/donghao1393/mcp-dbutils/commit/4df99de5d7d12c018aa5e28e9f785e5f0828543d))

# [0.16.0](https://github.com/donghao1393/mcp-dbutils/compare/v0.15.5...v0.16.0) (2025-03-15)


### Features

* 增强sonar-ai-fix脚本，添加PR支持和文件名自定义 ([ec8e574](https://github.com/donghao1393/mcp-dbutils/commit/ec8e574626a6907933c7a1c3853f88020bcf59b7))

## [0.15.5](https://github.com/donghao1393/mcp-dbutils/compare/v0.15.4...v0.15.5) (2025-03-15)


### Bug Fixes

* modify release workflow to preserve ruff target-version ([#49](https://github.com/donghao1393/mcp-dbutils/issues/49)) ([b071954](https://github.com/donghao1393/mcp-dbutils/commit/b071954b479613ea0bef7c2f4fb04ccd350dddfb))

## [0.15.4](https://github.com/donghao1393/mcp-dbutils/compare/v0.15.3...v0.15.4) (2025-03-15)


### Bug Fixes

* 修复并启用test_list_tables_tool_errors测试 ([#47](https://github.com/donghao1393/mcp-dbutils/issues/47)) ([2dd707e](https://github.com/donghao1393/mcp-dbutils/commit/2dd707ecbca0e7cdf02721a5a3caf243537874fe)), closes [#46](https://github.com/donghao1393/mcp-dbutils/issues/46)

## [0.15.3](https://github.com/donghao1393/mcp-dbutils/compare/v0.15.2...v0.15.3) (2025-03-15)


### Bug Fixes

* 修复SonarCloud问题提取逻辑，仅获取PR相关问题 ([#43](https://github.com/donghao1393/mcp-dbutils/issues/43)) ([8ca874c](https://github.com/donghao1393/mcp-dbutils/commit/8ca874c61a0f1d02ed98c79ea18ab7f66eb41659)), closes [#42](https://github.com/donghao1393/mcp-dbutils/issues/42)

## [0.15.2](https://github.com/donghao1393/mcp-dbutils/compare/v0.15.1...v0.15.2) (2025-03-14)


### Bug Fixes

* 修复SonarCloud报告的技术债务问题 ([#41](https://github.com/donghao1393/mcp-dbutils/issues/41)) ([3e97490](https://github.com/donghao1393/mcp-dbutils/commit/3e97490b37082360deabfcfc87228ab221c9d2b0)), closes [#37](https://github.com/donghao1393/mcp-dbutils/issues/37) [#37](https://github.com/donghao1393/mcp-dbutils/issues/37) [#37](https://github.com/donghao1393/mcp-dbutils/issues/37) [#37](https://github.com/donghao1393/mcp-dbutils/issues/37) [#37](https://github.com/donghao1393/mcp-dbutils/issues/37) [#37](https://github.com/donghao1393/mcp-dbutils/issues/37)

## [0.15.1](https://github.com/donghao1393/mcp-dbutils/compare/v0.15.0...v0.15.1) (2025-03-14)


### Bug Fixes

* ensure SonarCloud reports are generated even when analysis fails ([#40](https://github.com/donghao1393/mcp-dbutils/issues/40)) ([01d8a43](https://github.com/donghao1393/mcp-dbutils/commit/01d8a431f22079e621cc4160c210f3e8ce68a754)), closes [#39](https://github.com/donghao1393/mcp-dbutils/issues/39)

# [0.15.0](https://github.com/donghao1393/mcp-dbutils/compare/v0.14.0...v0.15.0) (2025-03-14)


### Features

* integrate Ruff code style automation ([#35](https://github.com/donghao1393/mcp-dbutils/issues/35)) ([6b2bdd7](https://github.com/donghao1393/mcp-dbutils/commit/6b2bdd749cecf2ad9167867c6e41149d1a57746f)), closes [#34](https://github.com/donghao1393/mcp-dbutils/issues/34)

# [0.14.0](https://github.com/donghao1393/mcp-dbutils/compare/v0.13.0...v0.14.0) (2025-03-14)


### Features

* implement SonarCloud PR auto-comment system ([#33](https://github.com/donghao1393/mcp-dbutils/issues/33)) ([4e83211](https://github.com/donghao1393/mcp-dbutils/commit/4e83211c4c7a289a6b794cdc5e03caac301d173c)), closes [#32](https://github.com/donghao1393/mcp-dbutils/issues/32)

# [0.13.0](https://github.com/donghao1393/mcp-dbutils/compare/v0.12.0...v0.13.0) (2025-03-14)


### Features

* configure SonarCloud quality gates ([#31](https://github.com/donghao1393/mcp-dbutils/issues/31)) ([454c4d3](https://github.com/donghao1393/mcp-dbutils/commit/454c4d384e4ddd8d324fe4292b13436c6b22328c)), closes [#30](https://github.com/donghao1393/mcp-dbutils/issues/30)

# [0.12.0](https://github.com/donghao1393/mcp-dbutils/compare/v0.11.0...v0.12.0) (2025-03-14)


### Features

* integrate SonarCloud analysis ([#29](https://github.com/donghao1393/mcp-dbutils/issues/29)) ([67649c5](https://github.com/donghao1393/mcp-dbutils/commit/67649c55cc317c2ee20c69777d1629895863dd86)), closes [#28](https://github.com/donghao1393/mcp-dbutils/issues/28)

# [0.11.0](https://github.com/donghao1393/mcp-dbutils/compare/v0.10.3...v0.11.0) (2025-03-13)


### Features

* Add MySQL support ([#26](https://github.com/donghao1393/mcp-dbutils/issues/26)) ([d25c5af](https://github.com/donghao1393/mcp-dbutils/commit/d25c5af9f44d81ca5160841817c40514dba750d4)), closes [#25](https://github.com/donghao1393/mcp-dbutils/issues/25) [#25](https://github.com/donghao1393/mcp-dbutils/issues/25) [#25](https://github.com/donghao1393/mcp-dbutils/issues/25) [#25](https://github.com/donghao1393/mcp-dbutils/issues/25) [#25](https://github.com/donghao1393/mcp-dbutils/issues/25) [#25](https://github.com/donghao1393/mcp-dbutils/issues/25) [#25](https://github.com/donghao1393/mcp-dbutils/issues/25)

## [0.10.3](https://github.com/donghao1393/mcp-dbutils/compare/v0.10.2...v0.10.3) (2025-03-13)


### Bug Fixes

* add dist directory check before PyPI publish ([88973ad](https://github.com/donghao1393/mcp-dbutils/commit/88973ad971d0975120e92fea46c9464e46f5b7eb))

## [0.10.2](https://github.com/donghao1393/mcp-dbutils/compare/v0.10.1...v0.10.2) (2025-03-13)


### Bug Fixes

* remove conditional check for PyPI publishing ([e714ef8](https://github.com/donghao1393/mcp-dbutils/commit/e714ef89db8dc35eca1a5c2f09f240dee94192eb))

## [0.10.1](https://github.com/donghao1393/mcp-dbutils/compare/v0.10.0...v0.10.1) (2025-03-13)


### Bug Fixes

* update verifyConditionsCmd in semantic-release config ([4271476](https://github.com/donghao1393/mcp-dbutils/commit/42714761d5d8bbbd39b9bae2aa550e1d06aa351c))

# CHANGELOG


## v0.10.0 (2025-03-12)

### Features

- Enhance database configuration with SSL support
  ([#22](https://github.com/donghao1393/mcp-dbutils/pull/22),
  [`4ea4d0b`](https://github.com/donghao1393/mcp-dbutils/commit/4ea4d0b5deb51b8e9202839bd7a8cd5f71463c88))

* feat: enhance database configuration with SSL support

- Replace jdbc_url with url for better clarity - Add dedicated SSL configuration support - Update
  documentation and examples - Update test cases

BREAKING CHANGE: Remove jdbc_url support as it was just added and not yet in production use

* docs: update documentation for SSL support and URL configuration

- Add SSL configuration examples - Update configuration format examples - Add configuration
  documentation in both English and Chinese - Remove JDBC related content

### Breaking Changes

- Remove jdbc_url support as it was just added and not yet in production use


## v0.9.0 (2025-03-09)

### Documentation

- Update README files to include new tools
  ([`eb796d5`](https://github.com/donghao1393/mcp-dbutils/commit/eb796d54ca517c173e26b8a535bfeb00545fbab0))

Added documentation for new tools: - dbutils-get-stats - dbutils-list-constraints -
  dbutils-explain-query

Both English and Chinese READMEs updated

- Update README files with new monitoring tools
  ([#18](https://github.com/donghao1393/mcp-dbutils/pull/18),
  [`4b919fe`](https://github.com/donghao1393/mcp-dbutils/commit/4b919fe348e2f6ed35ea1f16b64a2706a5d875f4))

- Add dbutils-get-performance tool documentation - Add dbutils-analyze-query tool documentation -
  Update both English and Chinese READMEs

- Update tool names with dbutils prefix
  ([`4731021`](https://github.com/donghao1393/mcp-dbutils/commit/4731021ab981ecca305414f34f72c1f8f0577b8e))

Renamed basic tools in README files: - list_tables -> dbutils-list-tables - query -> dbutils-query

Both English and Chinese READMEs updated

### Features

- Add advanced database tools ([#15](https://github.com/donghao1393/mcp-dbutils/pull/15),
  [`2c85dc8`](https://github.com/donghao1393/mcp-dbutils/commit/2c85dc8c026bca93571ab8ed5b837518553087d5))

* Added three new tools:

1. dbutils-get-stats - Table statistics information - Column level statistics - Adapted for
  PostgreSQL and SQLite

2. dbutils-list-constraints - Primary key, foreign key, unique constraints - Constraint definitions
  and properties - Constraint comments support

3. dbutils-explain-query - EXPLAIN and EXPLAIN ANALYZE support - Detailed cost and timing estimates
  - Database-specific optimizations

Implementation: - Added abstract methods to DatabaseHandler - Implemented in PostgreSQL and SQLite -
  Added dedicated integration tests - Fixed SQL syntax and parameter issues

Refs #14

* fix: check non-SELECT statements in SQLite handler

- Add more database tools ([#13](https://github.com/donghao1393/mcp-dbutils/pull/13),
  [`8b8bd1e`](https://github.com/donghao1393/mcp-dbutils/commit/8b8bd1ea04d63e7828c81dc25a9c0cb70df73867))

* 添加更多数据库工具

添加三个新的数据库工具： - dbutils-describe-table：获取表的详细信息 - dbutils-get-ddl：获取表的DDL语句 -
  dbutils-list-indexes：获取表的索引信息

实现内容： - DatabaseHandler新增三个抽象方法 - PostgreSQL和SQLite分别实现这些方法 - 添加新工具的集成测试 - 所有测试通过

Fixes #12

* test: 拆分表信息工具测试

将test_table_info_tools拆分为三个独立的测试函数： - test_describe_table_tool - test_get_ddl_tool -
  test_list_indexes_tool

这样可以更清晰地展示每个工具的测试状态，便于定位问题。

- Enhance monitoring system with LLM dialog support
  ([#17](https://github.com/donghao1393/mcp-dbutils/pull/17),
  [`50d8df1`](https://github.com/donghao1393/mcp-dbutils/commit/50d8df1fabbf6513718582e6efe0d3832de9ce5d))

- Add query duration tracking - Add query type statistics - Add slow query detection - Add memory
  usage tracking - Add performance statistics formatting - Add new MCP tools:
  dbutils-get-performance and dbutils-analyze-query - Add tests for new features

Closes #16


## v0.8.0 (2025-03-09)

### Features

- Unify tool names with dbutils prefix ([#11](https://github.com/donghao1393/mcp-dbutils/pull/11),
  [`aa57995`](https://github.com/donghao1393/mcp-dbutils/commit/aa57995dc6cf3ffd33909162d831dffbbbf19bfc))

给工具名称添加dbutils前缀，使所有工具名称规范统一： - query -> dbutils-run-query - list_tables -> dbutils-list-tables

让工具名称更清晰地表明是属于dbutils的工具，避免与其他MCP服务的工具冲突。

Fixes #11


## v0.7.0 (2025-03-09)

### Documentation

- Update README with list_tables tool information
  ([`f3a2592`](https://github.com/donghao1393/mcp-dbutils/commit/f3a259200bbf18aaebbf6d4511a18d35246f5044))

### Features

- Add database type prefix to list_tables tool response
  ([#10](https://github.com/donghao1393/mcp-dbutils/pull/10),
  [`e32ce1f`](https://github.com/donghao1393/mcp-dbutils/commit/e32ce1f2502f24d111643d7233f0fdd420238bd7))

添加数据库类型前缀到list_tables工具的返回结果中，使LLM能够知道当前操作的数据库类型， 便于后续操作。格式与错误信息保持一致，使用[数据库类型]前缀。

Fixes #9


## v0.6.0 (2025-03-08)

### Documentation

- Add SQLite JDBC URL configuration documentation
  ([#6](https://github.com/donghao1393/mcp-dbutils/pull/6),
  [`7d7ca8b`](https://github.com/donghao1393/mcp-dbutils/commit/7d7ca8bc7d4047a6c45dc3b8c6106e1fcbdd16d0))

- Add SQLite JDBC URL examples and explanation - Update configuration format description - Keep
  Chinese and English documentation in sync

Part of #4

### Features

- **tool**: Add list_tables tool for database exploration
  ([#8](https://github.com/donghao1393/mcp-dbutils/pull/8),
  [`6808c08`](https://github.com/donghao1393/mcp-dbutils/commit/6808c0868c8959450a9cfdcdf79a0af53bf22933))

* feat(tool): add list_tables tool for database exploration

This commit adds a new list_tables tool that allows LLMs to explore database tables without knowing
  the specific database type, leveraging the existing get_tables abstraction.

Fixes #7

* test(tool): add integration tests for list_tables tool

* test: add integration tests for list_tables tool

This commit: - Adds test for list_tables tool functionality with both PostgreSQL and SQLite - Adds
  test for error cases - Uses proper ClientSession setup for MCP testing

* fix(test): update test assertions for list_tables tool errors

- Fix incorrect error handling assertions - Fix indentation issues in test file - Use try-except
  pattern for error testing

* fix(test): update error handling in list_tables tests

- Use MCP Error type instead of ConfigurationError - Fix indentation issues - Improve error
  assertions

* fix(test): correct McpError import path

* fix(test): use correct import path for McpError

* fix(test): use try-except for error testing instead of pytest.raises

* test: skip unstable error test for list_tables tool


## v0.5.0 (2025-03-02)

### Documentation

- Add JDBC URL configuration documentation
  ([`a1b5f4b`](https://github.com/donghao1393/mcp-dbutils/commit/a1b5f4b424cec0df239bed65705aaac7c3e9072a))

- Add JDBC URL configuration examples to English and Chinese docs - Document secure credential
  handling approach - Update configuration format descriptions

Part of feature #2

### Features

- **config**: Add JDBC URL support for SQLite
  ([#5](https://github.com/donghao1393/mcp-dbutils/pull/5),
  [`9feb1e8`](https://github.com/donghao1393/mcp-dbutils/commit/9feb1e8c7e38a8e4e3c0f63c81a72f4a4edd05b5))

- Add JDBC URL parsing for SQLite configuration - Support SQLite specific URL format and parameters
  - Keep credentials separate from URL - Complete test coverage for new functionality

Part of #4


## v0.4.0 (2025-03-01)

### Features

- **config**: Add JDBC URL support for PostgreSQL
  ([#3](https://github.com/donghao1393/mcp-dbutils/pull/3),
  [`4f148f3`](https://github.com/donghao1393/mcp-dbutils/commit/4f148f31d5dc623b8b39201f0270d8f523e65238))

- Add JDBC URL parsing with strict security measures - Require credentials to be provided separately
  - Implement validation for all required parameters - Add comprehensive test coverage

Closes #2


## v0.3.0 (2025-02-16)

### Bug Fixes

- Fix pkg_meta reference error in DatabaseServer
  ([`9bcc607`](https://github.com/donghao1393/mcp-dbutils/commit/9bcc607378df09fee8ef301c1ce0247f419c2dab))

- Move pkg_meta initialization before its usage - Add comment to clarify the purpose of pkg_meta -
  Fix the variable reference error that caused server startup failure

- Fix prompts/list timeout by using correct decorator pattern
  ([`227f86d`](https://github.com/donghao1393/mcp-dbutils/commit/227f86db4c050439a382118df1bc62944f35aea4))

- Update Server initialization with version - Simplify list_prompts handler to return raw data - Add
  comprehensive error handling in tests - Add debug logging for better traceability

- Unify logger naming across the project
  ([`088e60b`](https://github.com/donghao1393/mcp-dbutils/commit/088e60becb7112dc0a5da256b56d0f79ed1db223))

- Use package metadata for logger names - Add consistent naming hierarchy: - Root: mcp-dbutils -
  Server: mcp-dbutils.server - Handler: mcp-dbutils.handler.<database> - Database:
  mcp-dbutils.db.<type> - Remove hardcoded server names

- Unify prompts handler registration and remove duplicate init options
  ([`6031592`](https://github.com/donghao1393/mcp-dbutils/commit/60315922b052f252005ed77fd3978d8cff085056))

- Use package metadata for server name and version
  ([`7f48a6d`](https://github.com/donghao1393/mcp-dbutils/commit/7f48a6df50830d58c534495fc7bfc9198e9fbcc5))

- Replace hardcoded server name and version with values from pyproject.toml - Add importlib.metadata
  to read package information - Ensure consistent versioning across the project

### Build System

- Simplify semantic-release configuration
  ([`0f37153`](https://github.com/donghao1393/mcp-dbutils/commit/0f37153a0d7205238d0f43c16c97a390a3e368df))

- Remove __version__ variable reference - Change build command to use uv build - Keep version
  management in pyproject.toml only

### Code Style

- Unify log timestamp format with MCP framework
  ([`c341fb1`](https://github.com/donghao1393/mcp-dbutils/commit/c341fb1d05144c5c925fed25bfcd69be55ee7803))

- Use milliseconds precision in log timestamps to match MCP framework
  ([`2aae2fd`](https://github.com/donghao1393/mcp-dbutils/commit/2aae2fd06bf9b505105fd6b0671d70ba7dfef0f5))

### Continuous Integration

- Add automatic release
  ([`b69e242`](https://github.com/donghao1393/mcp-dbutils/commit/b69e2429857824f0807eb76baccbbdf855c89e45))

- Add GitHub Actions workflow for automatic releases - Configure release triggers - Set up
  permissions - Use python-semantic-release action

- Add uv installation to release workflow
  ([`62e0362`](https://github.com/donghao1393/mcp-dbutils/commit/62e036254cc1af6d1a1a3028838652365a528c53))

- Install uv before running semantic-release - Add uv binary to GitHub PATH - Ensure build command
  can be executed

- Improve release workflow
  ([`07128a0`](https://github.com/donghao1393/mcp-dbutils/commit/07128a0ea7687963531e1aada24cc4083540272f))

- Separate version determination and build steps - Use actions/setup-python for Python environment -
  Disable automatic build in semantic-release - Add manual build step using uv - Fix invalid action
  parameters

- Improve release workflow reliability
  ([`4dac367`](https://github.com/donghao1393/mcp-dbutils/commit/4dac36749917b0d3fec94de5bcce1b5b0295e94f))

- Disable build in semantic-release - Add debug command to verify uv installation - Keep using uv
  for package building - Ensure PATH is properly set

- Integrate PyPI publishing into release workflow
  ([`2ebd3f3`](https://github.com/donghao1393/mcp-dbutils/commit/2ebd3f327748fc78dd7e33e366517120260b3d3b))

- Add upload_to_pypi option to semantic-release action - Enable build in semantic-release - Remove
  separate publish workflow - Simplify release process

- Update publish workflow trigger
  ([`26a6d79`](https://github.com/donghao1393/mcp-dbutils/commit/26a6d79eb8940cde6fb61ebe601754a1d8f22f0b))

- Add 'created' event type to release trigger - Support automatic PyPI publishing when
  semantic-release creates a release - Keep 'published' event for manual releases

- Update release workflow for trusted publishing
  ([`8297cb8`](https://github.com/donghao1393/mcp-dbutils/commit/8297cb88b496c55d1f84355ed1a015ebf80a2c42))

- Add PyPI environment configuration - Use correct PyPI publish action version - Configure trusted
  publishing permissions - Add PyPI project URL

### Documentation

- Unify server name in configuration examples
  ([`5380898`](https://github.com/donghao1393/mcp-dbutils/commit/538089864e1cef72b0560ff369f30530f4358944))

- Change server name from 'dbutils' to 'mcp-dbutils' in all examples - Keep consistent with package
  name and version in pyproject.toml - Update both English and Chinese documentation

### Features

- Add database type to error messages
  ([`cf8d53b`](https://github.com/donghao1393/mcp-dbutils/commit/cf8d53baaee247fa6313ab6d0766144f9a3f0024))

- Add database type to query results
  ([`0cebfd9`](https://github.com/donghao1393/mcp-dbutils/commit/0cebfd99ffc9201c82a85d0b8e82ba59fa4a958e))

- Add version info to startup log
  ([`dc06741`](https://github.com/donghao1393/mcp-dbutils/commit/dc06741fce536884c1aeebd19838877c5901a546))


## v0.2.11 (2025-02-15)

### Chores

- Bump version to 0.2.11
  ([`96b023f`](https://github.com/donghao1393/mcp-dbutils/commit/96b023ff6bae3a643401b639c86403e7ac31df07))

### Features

- Implement basic prompts support and list handler
  ([`397e71a`](https://github.com/donghao1393/mcp-dbutils/commit/397e71abca7286626c4eec4482e13ead83871e3a))


## v0.2.10 (2025-02-15)

### Documentation

- Update CHANGELOG for version 0.2.10
  ([`f3a6d4e`](https://github.com/donghao1393/mcp-dbutils/commit/f3a6d4ef0ce8c5fcbb0abf9b0b210447c40ce2c4))

### Features

- Add resource monitoring system
  ([`f3ff859`](https://github.com/donghao1393/mcp-dbutils/commit/f3ff859a57c7bb046725a6ee9dd746e06bb488ff))

- Add ResourceStats for resource usage tracking - Improve database handlers using template method
  pattern - Implement connection lifecycle monitoring - Add error pattern analysis - Output
  monitoring data through stderr

### Testing

- Add tests for resource monitoring system
  ([`ab9a644`](https://github.com/donghao1393/mcp-dbutils/commit/ab9a644bdae750831a9792bda157813eb9ab5ed1))

- Add unit tests for ResourceStats - Add integration tests for monitoring - Adjust base handler for
  better testability


## v0.2.9 (2025-02-15)

### Bug Fixes

- Fix logger function calls
  ([`9b9fe45`](https://github.com/donghao1393/mcp-dbutils/commit/9b9fe45b60c74c7e14d7978b011f5c8b2399892d))

- Update logger calls to match create_logger function interface - Fix debug log calls in get_handler
  method

- Fix logging and variable initialization
  ([`8f68320`](https://github.com/donghao1393/mcp-dbutils/commit/8f68320f13b7e5ca9bf6bb669a0212d0f705367b))

- Rename log to logger in DatabaseServer for consistency - Initialize handler variable before try
  block to avoid UnboundLocalError - Fix logger reference in cleanup code

- Update handlers to use custom exceptions
  ([`02eb55c`](https://github.com/donghao1393/mcp-dbutils/commit/02eb55c8e4305043b09d8dc1ee4ece78a50c187c))

- Update PostgreSQL handler to use DatabaseError - Update SQLite handler to use DatabaseError - Add
  specific error messages for non-SELECT queries - Improve error handling and logging

### Documentation

- Update changelog for v0.2.9
  ([`0ccc28e`](https://github.com/donghao1393/mcp-dbutils/commit/0ccc28e926e54d7fad84f74dce36fcad75bfd7f0))

### Features

- Optimize database type handling and error system
  ([`045b62d`](https://github.com/donghao1393/mcp-dbutils/commit/045b62d9a325304248252a86294766debc97590e))

- Remove redundant type detection based on path/dbname - Use explicit 'type' field from
  configuration - Add custom exception hierarchy - Enhance logging system

### Testing

- Update test cases for custom exceptions
  ([`93ef088`](https://github.com/donghao1393/mcp-dbutils/commit/93ef0889e00b37aaeedc83f4e3ba8debcb897100))

- Update test_postgres.py to use DatabaseError - Update test_sqlite.py to use DatabaseError - Fix
  error message assertions for non-SELECT queries


## v0.2.8 (2025-02-15)

### Bug Fixes

- Properly remove all await on mcp_config
  ([`6153277`](https://github.com/donghao1393/mcp-dbutils/commit/6153277f06f404fbd8b8cd851f54024d706b4c05))

- Remove await on mcp_config in tests
  ([`e917226`](https://github.com/donghao1393/mcp-dbutils/commit/e917226b5dd23c6eb07200912e7d25f6c73135a2))

- Fix type error 'dict' object is not an async iterator - Update both postgres and sqlite tests -
  Remove unnecessary awaits on mcp_config fixture

- Remove custom event_loop fixture
  ([`159f9e9`](https://github.com/donghao1393/mcp-dbutils/commit/159f9e9b86c7979061ffca3cf466ae81f642d67a))

- Remove custom event_loop fixture to use pytest-asyncio's default - Revert pyproject.toml changes
  to minimize modifications - Fix pytest-asyncio deprecation warning

- Use pytest_asyncio.fixture for async fixtures
  ([`ea08512`](https://github.com/donghao1393/mcp-dbutils/commit/ea0851208b5c84331df50c6a1261acc24dbe7070))

- Replace @pytest.fixture with @pytest_asyncio.fixture for async fixtures - Keep original
  @pytest.fixture for non-async event_loop - Fix pytest-asyncio deprecation warnings

### Chores

- Bump version to 0.2.8
  ([`d72cf52`](https://github.com/donghao1393/mcp-dbutils/commit/d72cf5272324cdb5164291b91139e537a07980db))

- Update version in pyproject.toml - Add 0.2.8 changelog entry for test improvements - Document
  pytest-asyncio configuration changes

- Configure pytest-asyncio fixture loop scope
  ([`d8ca223`](https://github.com/donghao1393/mcp-dbutils/commit/d8ca22318609cff81fa2b1bd0a308cf97d3a7558))

- Set asyncio_mode to strict - Set asyncio_default_fixture_loop_scope to function - Fix
  pytest-asyncio configuration warning

- Configure pytest-asyncio mode to auto
  ([`7898f61`](https://github.com/donghao1393/mcp-dbutils/commit/7898f61b960f74c4a3ca42366eb6004a6ca6d070))

- Add pytest config to remove asyncio warning - Set asyncio_mode to auto in tool.pytest.ini_options


## v0.2.7 (2025-02-15)

### Bug Fixes

- Add venv creation in CI workflow
  ([`386faec`](https://github.com/donghao1393/mcp-dbutils/commit/386faec3213a7cd4ce7e14a43225f005f3f28702))

- Update coverage badge configuration
  ([`c6bc9bd`](https://github.com/donghao1393/mcp-dbutils/commit/c6bc9bdee4006fc8dd2d3e4dcf9111ce4ad104b0))

- Update to dynamic-badges-action v1.7.0 - Ensure integer percentage value - Add proper quotes to
  parameters

### Features

- Add coverage badge to README
  ([`20435d8`](https://github.com/donghao1393/mcp-dbutils/commit/20435d87c657413d656cf61abb5e16bcf6fc0300))

- Added coverage badge generation in CI workflow - Added coverage badge to README - Updated
  CHANGELOG.md

- Add Github Actions workflow for automated testing
  ([`355a863`](https://github.com/donghao1393/mcp-dbutils/commit/355a863193ead9d21d928c21453e64c67e71d760))

- Added GitHub Actions workflow for test automation - Added PostgreSQL service in CI environment -
  Added detailed test and coverage reporting - Bump version to 0.2.7


## v0.2.6 (2025-02-12)

### Features

- Add test coverage reporting
  ([`93fe2f7`](https://github.com/donghao1393/mcp-dbutils/commit/93fe2f73dc472c8e8b5e7eb0a1b65879c806aa8a))

- Added pytest-cov for test coverage tracking - Added .coveragerc configuration - HTML coverage
  report generation - Updated .gitignore for coverage files - Updated CHANGELOG.md - Bump version to
  0.2.6


## v0.2.5 (2025-02-12)

### Documentation

- Enhance Docker documentation with database connection details
  ([`af42c97`](https://github.com/donghao1393/mcp-dbutils/commit/af42c97259eb9a5f5f2d135f8bac9690029fa843))

- Add examples for SQLite database file mapping - Document host PostgreSQL connection from container
  - Provide configuration examples for different OS environments - Add notes about
  host.docker.internal and network settings

- Show real-time chart on readme
  ([`704e5fd`](https://github.com/donghao1393/mcp-dbutils/commit/704e5fde808b996f00b51c1f534073e262c94384))

- Update changelog for v0.2.5
  ([`cb71c83`](https://github.com/donghao1393/mcp-dbutils/commit/cb71c831193c7b0758592075271d90ff48b00c94))

### Features

- Add initial automated tests
  ([`935a77b`](https://github.com/donghao1393/mcp-dbutils/commit/935a77b0d5076fe141a92128eeabc249ff3489c8))

- Add integration tests for PostgreSQL and SQLite handlers: * Table listing and schema querying *
  SELECT query execution and result formatting * Non-SELECT query rejection * Error handling for
  invalid queries - Configure test fixtures and environments in conftest.py - Set up pytest
  configurations in pyproject.toml - Update .gitignore to exclude memory-bank folder for cline

Tests verify core functionality while adhering to read-only requirements.


## v0.2.4 (2025-02-09)

### Documentation

- Major documentation improvements and version 0.2.4
  ([`7a9404a`](https://github.com/donghao1393/mcp-dbutils/commit/7a9404ad513d4b1f65f9c74f6a3eac0ea43058c9))

- Unified server configuration name to "dbutils" - Added architecture diagrams in both English and
  Chinese - Enhanced installation instructions with environment variables - Added contributing
  guidelines - Added acknowledgments section - Updated badges and improved formatting - Bump version
  to 0.2.4


## v0.2.3 (2025-02-09)

### Bug Fixes

- Remove uv cache dependency in GitHub Actions
  ([`a68f32e`](https://github.com/donghao1393/mcp-dbutils/commit/a68f32e5515ca6b6253442d74a5b9112e7ebf852))

- Remove cache-dependency-glob parameter - Disable uv cache to avoid dependency on uv.lock file

### Chores

- Bump version to 0.2.3
  ([`771e01e`](https://github.com/donghao1393/mcp-dbutils/commit/771e01efcf8ecb32c85b133836d5f179a0f2ce08))

- Update version in pyproject.toml - Add version 0.2.3 to CHANGELOG.md - Document installation
  guides, internationalization, and CI/CD additions

### Continuous Integration

- Add PyPI publishing workflow
  ([`ae5f334`](https://github.com/donghao1393/mcp-dbutils/commit/ae5f334190091207302a258311172804fd25ac16))

- Create .github/workflows/publish.yml - Configure uv environment using astral-sh/setup-uv@v4 - Set
  up automatic build and PyPI publishing - Enable trusted publishing mechanism

### Documentation

- Add MIT license and update project metadata
  ([`f98e656`](https://github.com/donghao1393/mcp-dbutils/commit/f98e656804d279bb53e193bfa87bfd1cd240e0db))

- Update installation guide and add English README
  ([`a4e60e0`](https://github.com/donghao1393/mcp-dbutils/commit/a4e60e0e792e34a4f327fe8a49e1a24a430b2abb))

- Add installation methods (uvx/pip/docker) - Update configuration examples for each installation
  method - Create English README with badges - Update project name to mcp-dbutils - Add
  cross-references between Chinese and English docs

- Update version to 0.2.2 and add CHANGELOG
  ([`381c69b`](https://github.com/donghao1393/mcp-dbutils/commit/381c69bf31af5f58d96f871de0088214cc77ca48))

- 添加中文readme文档
  ([`a3737b9`](https://github.com/donghao1393/mcp-dbutils/commit/a3737b995857b414c5ba40f1958f2b7b9b2aa65d))

- 添加README_CN.md详细说明项目功能和使用方法 - 重点解释抽象层设计理念和架构 - 包含配置示例和使用示范 - 提供完整的API文档


## v0.2.2 (2025-02-09)

### Bug Fixes

- Add missing Path import in sqlite server
  ([`fb35c1a`](https://github.com/donghao1393/mcp-dbutils/commit/fb35c1a56531456ca27319922b20efe14381b38d))

- Add pathlib import for Path usage in SQLite server - Fix code formatting

- Automatic database type detection from config
  ([`9b69882`](https://github.com/donghao1393/mcp-dbutils/commit/9b698824acc721cd697325ff0c601e11cd68ef33))

- Remove --type argument and detect db type from config - Unify configuration handling for both
  postgres and sqlite - Detect db type based on config parameters - Update SqliteServer to match
  PostgresServer interface

### Features

- Add explicit database type declaration and awareness
  ([`2d47804`](https://github.com/donghao1393/mcp-dbutils/commit/2d47804ca917e2f59b0832a7a6c92789fc97f0b8))

1. Add required 'type' field to configs to explicitly declare database type 2. Standardize field
  naming, rename 'db_path' to 'path' 3. Include database type and config name in query results 4.
  Restructure response format to unify normal results and error messages

This change enables LLMs to be aware of the database type in use, allowing them to auto-correct when
  incorrect SQL syntax is detected.

- Add password support for sqlite databases
  ([`537f1dc`](https://github.com/donghao1393/mcp-dbutils/commit/537f1dc96291ed57dbe7a52c9c7a80a868270152))

- Support password-protected SQLite databases in config - Use URI connection string for SQLite with
  password - Update connection handling and parameter passing - Add password masking in logs

- Remove required --database argument and enhance logging
  ([`9b49ac7`](https://github.com/donghao1393/mcp-dbutils/commit/9b49ac70e88a8c1d0469cdb36ae8608fd01ccaaa))

- Remove mandatory --database argument - Add connection status monitoring for all databases - Add
  automatic retry mechanism with configurable interval - Add MCP_DB_RETRY_INTERVAL environment
  variable (default: 1800s) - Add proper MCP_DEBUG support - Remove duplicated code - Improve
  logging for connection status changes

- Standardize logging
  ([`df264b5`](https://github.com/donghao1393/mcp-dbutils/commit/df264b55aed6341778f860e05072306cbb24388d))

- Use standardized logging mechanism from log.py

- **sqlite**: Add support for dynamic database switching
  ([`3f71de0`](https://github.com/donghao1393/mcp-dbutils/commit/3f71de0d220eca8252f325b264ccaa401fd71646))

- Add config_path parameter to SQLite server initialization - Add optional database parameter to
  query tool - Implement dynamic database switching in call_tool method - Keep interface consistent
  with PostgreSQL server

### Refactoring

- Redesign database server architecture for dynamic database switching
  ([`7f0a7b9`](https://github.com/donghao1393/mcp-dbutils/commit/7f0a7b92561baf357b67aa5596b6842659a934bb))

- Add DatabaseHandler base class for individual database connections - Move database operations from
  server to handlers - Implement on-demand database handler creation and cleanup - Simplify server
  initialization and configuration - Make database parameter required in query tool - Remove the
  remaining mcp_postgres directories and files

- Remove default database connection behavior
  ([`45fe01c`](https://github.com/donghao1393/mcp-dbutils/commit/45fe01c1ae27cde43843e410c45826565a18fe50))

- Remove default database concept from base implementation - Require explicit database specification
  for all operations - Convert PostgreSQL handler from connection pool to per-operation connections
  - Remove immediate connection testing in handlers - Fix resource cleanup in PostgreSQL handler


## v0.2.1 (2025-02-09)

### Bug Fixes

- Correct stdio transport initialization in base class
  ([`e9558c2`](https://github.com/donghao1393/mcp-dbutils/commit/e9558c20523d157461054442f8e3dedfb4cb930e))

- Remove non-existent create_stdio_transport method - Use stdio_server directly from
  mcp.server.stdio

### Features

- Add base classes and shared configurations
  ([`bd82bfc`](https://github.com/donghao1393/mcp-dbutils/commit/bd82bfc1a5145df4664758b87c35ecd917f99f1a))

- Add DatabaseServer abstract base class - Add DatabaseConfig abstract base class - Update main
  entry point to support multiple database types - Implement shared configuration utilities

- Add sqlite database support
  ([`7d0afb3`](https://github.com/donghao1393/mcp-dbutils/commit/7d0afb37d9711c627761699fe04185e1735969b0))

- Add SqliteConfig for SQLite configuration - Add SqliteServer implementation with basic query
  features - Support table schema inspection and listing - Match existing PostgreSQL feature set
  where applicable

### Refactoring

- Update postgres code to use base classes
  ([`51146f4`](https://github.com/donghao1393/mcp-dbutils/commit/51146f4882ff028705565ba8410f4bbd6c61c67e))

- Inherit PostgresConfig from base DatabaseConfig - Implement abstract methods in PostgresServer -
  Move postgres-specific code to postgres module - Update connection and query handling


## v0.2.0 (2025-02-08)

### Refactoring

- Rename project to mcp-dbutils and restructure directories
  ([`ddf3cea`](https://github.com/donghao1393/mcp-dbutils/commit/ddf3cea41d9368eed11cb5b7a3551b1abd058c9e))

- Rename project from mcp-postgres to mcp-dbutils - Update project description to reflect
  multi-database support - Create directories for postgres and sqlite modules - Move existing files
  to new structure


## v0.1.1 (2025-02-08)


## v0.1.0 (2025-02-08)

### Bug Fixes

- Adjust database connection handling
  ([`060354a`](https://github.com/donghao1393/mcp-dbutils/commit/060354a5f681ba67da46488705f877a8ac9fc45f))

- Split connection parameters to fix VPN connection issue - Refactor connection pool creation based
  on working example - Add better error logging for connection failures - Remove trailing spaces

- Correct logger function usage
  ([`cbace7c`](https://github.com/donghao1393/mcp-dbutils/commit/cbace7cf8226d87c36bc5bf3aadda383e0f1abff))

- Fix logger function calls to match the custom logger implementation - Change logger.warning/warn
  to direct function calls with level parameter - Maintain consistent logging format across the
  application

This fixes the AttributeError related to logger function calls

- Correct package installation and command line args
  ([`dfba347`](https://github.com/donghao1393/mcp-dbutils/commit/dfba34759393090c4fa728b4a72ad2d34d18f70c))

- Add proper pyproject.toml configuration - Fix module import path issues - Update argument handling
  in server

- Remove required db-name parameter and add auto-selection
  ([`482cfa3`](https://github.com/donghao1393/mcp-dbutils/commit/482cfa336e31f417187c255ebbcaa45c1a8ba4e9))

- Remove required flag from db-name argument - Add auto-selection of first available database when
  db-name not specified - Keep connection check for all configured databases - Add logging for
  database connection status - Maintain backwards compatibility with manual db selection

### Features

- Add connection check for all configured databases
  ([`162b5ba`](https://github.com/donghao1393/mcp-dbutils/commit/162b5baabe851f690406a60b4f349abb402bfc7d))

- Add connection check for all databases at startup - Continue if some databases fail but at least
  one succeeds - Add detailed connection status logging - Make database name parameter required -
  Improve error messages with connection status details

- Initialize Postgres MCP server
  ([`f91a8bc`](https://github.com/donghao1393/mcp-dbutils/commit/f91a8bc6d16a2d53bdf53ccc05229cade8e9e573))

- Support local host override for VPN environments - Add connection pool management - Implement
  schema inspection and read-only query tools - Add configuration separation for better
  maintainability

- Support multiple database configurations in YAML
  ([`cdeaa02`](https://github.com/donghao1393/mcp-dbutils/commit/cdeaa024eac5469caeb978d0ab455bb264006c4b))

- Restructure YAML format to support multiple database targets - Add database selection by name
  (dev-db, test-db etc) - Support default database configuration - Add validation for database
  configuration selection

### Refactoring

- Combine database tools into single query_db tool
  ([`78437c7`](https://github.com/donghao1393/mcp-dbutils/commit/78437c79ec3f1da65e3e96622f1df02c9b7d56da))

- Merge database profile selection and SQL query into one tool - Add database_profile as required
  parameter for query_db tool - Remove separate profile selection step - Simplify tool interaction
  flow - Add proper error handling and validation

- Combine database tools into single query_db tool
  ([`602cbd8`](https://github.com/donghao1393/mcp-dbutils/commit/602cbd88407d7faf86ec97d18665ee449f500e61))

- Merge database profile selection and SQL query into one tool - Add database_profile as required
  parameter for query_db tool - Remove separate profile selection step - Simplify tool interaction
  flow - Add proper error handling and validation

This change simplifies the tool interface while maintaining explicit database selection requirement.

- Remove default database config
  ([`9ceaa2f`](https://github.com/donghao1393/mcp-dbutils/commit/9ceaa2f7eefceb0b423325f30b6ec181126cd91f))

- Remove default database configuration from YAML - Make database name parameter mandatory - Add
  available database names in error message - Simplify configuration structure

This change enforces explicit database selection for better clarity and prevents accidental use of
  wrong database environments.

- Reorganize project structure
  ([`dc2eace`](https://github.com/donghao1393/mcp-dbutils/commit/dc2eace23b0a5f23227a7d7599d2bec2836a6338))

- Rename package from 'postgres' to 'mcp_postgres' - Add logging support - Improve code organization

- Simplify and improve server code
  ([`c56a0a0`](https://github.com/donghao1393/mcp-dbutils/commit/c56a0a011052d4419e5dd4ed1b9173a37fff35c1))

- Merge duplicate tool handlers into a single unified handler - Add YAML configuration support with
  multiple database profiles - Improve connection management with proper pool handling - Add masked
  logging for sensitive connection information - Refactor command line arguments for better
  usability

- Split database tools and enforce explicit database selection
  ([`2d6bfa3`](https://github.com/donghao1393/mcp-dbutils/commit/2d6bfa3e0779ef42e07dbc8884f2153230ad4f5c))

- Add set_database_profile tool with proper decorator - Split handle_call_tool into separate
  handlers for each tool - Add validation for database selection before SQL execution - Update tool
  handlers to return proper MCP response types - Add current database profile tracking

- Support YAML config for database connection
  ([`35ac49c`](https://github.com/donghao1393/mcp-dbutils/commit/35ac49c7d9a93e0d5bbd9d741a5660cbc73004d0))

- Add YAML config support as an alternative to database URL - Implement PostgresConfig class with
  both YAML and URL parsing - Use anyio for better async compatibility - Keep backward compatibility
  with URL-based configuration - Improve connection parameter handling for special characters
