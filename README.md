# Equipment-monitoring-System

Equipment monitoring System
Система позволяет пользователю мониторить состояние выбранного оборудования. Система состоит из сервиса оборудования (конкретных экземпляров с серийными номерами) и моделей (классов) оборудования, сервиса, имитирующего получение данных с экземпляров оборудования, и экранов мониторинга, отображающего данные по оборудованию для пользователей.

Бизнес сервисы:
Табло мониторинга (Monitor Service)
Оборудование (Equipment Service)
Файловое хранилище документов по оборудованию (Documentation Service)
Данные с оборудования (Generator Service)
Дополнительные сервисы:
Gateway
Авторизация (Session Service)
Админка (Report Service)
Структуры данных
User (Session Service):
+ login
+ password
+ user_uid

Monitor (Monitor Service):
+ monitor_uid
+ name
+ [equipment_uid] -> FK to Equipment Service (Equipment::equipment_uid)
+ [equipment_models_uid] -> FK to Equipment Service (EquipmentModel::equipment_models_uid)
+ [params] -> FK to Equipment Service (EquipmentModel::params)

Equipment (Equipment Service):
+ equipment_uid
+ [model_uid] -> FK to Equipment Service (EquipmentModel::equipment_model_uid)
+ status

Equipment Model (Equipment Service):
+ equipment_model_uid
+ [params]

Files (Documentation Service):
+ file_uid
+ file_name
+ content
+ equipment_model_uid -> FK to Equipment Service (EquipmentModel::equipment_model_uid)


DataGenerator (Generator Service):
+ data_uid
+ equipment_uid -> FK to Equipment Service (Equipment::equipment_uid)
+ value
+ param
(!) Указанный набор полей характерен для “получаемой с оборудования информации”, использование базы данных в данном сервисе определяется студентом на этапе проектирования.
Основные операции
Специфические для варианта задания:
Список экранов мониторинга. [G]
GET /monitors
Экран мониторинга. [G]
GET /monitors/{monitorUid}
Настройка экрана мониторинга. [S][M][G]
header: Authorization: bearer <jwt>
POST /monitor
body: { monitorUid, name, [equipment_uid], [equipment_models_uid], [params] }
Добавить модель оборудования. [A][M][G]
header: Authorization: bearer <jwt>
POST /equipment-model
Создать экземпляр оборудования. [A][M][G]
header: Authorization: bearer <jwt>
POST /equipment
body: { … }
Изменить статус оборудования (активировать, деактивировать, списать). [A][M][G]
header: Authorization: bearer <jwt>
POST /equipment/{equipmentUid}/{activate/deactivate/remove}
Просмотр модели оборудования. [S][G]
header: Authorization: bearer <jwt>
GET /model/{equipmentModelUid}
Просмотр конкретного оборудования. [S][G]
header: Authorization: bearer <jwt>
GET /equipment/{equipmentUid}
Посмотреть статистику по “популярности” оборудования (на скольких экранах отслеживается). [A][G]
header: Authorization: bearer <jwt>
GET /reports/equipment-popular
Посмотреть статистику по количеству работающего оборудования. [A][G]
header: Authorization: bearer <jwt>
GET /reports/equipment-active
