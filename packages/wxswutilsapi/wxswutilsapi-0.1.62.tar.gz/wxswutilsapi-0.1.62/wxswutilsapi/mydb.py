# authlib/db_helper.py

from datetime import datetime
import uuid
from sqlalchemy.exc import SQLAlchemyError

class mydb:
    def __init__(self, db_session):
        self.db = db_session

    def fetch_all_by(self, model, params, fields=None, no_total=False, field_mappings={}):
        try:
            filters = {}
            start_time = params.get('startTime')
            end_time = params.get('endTime')

            if start_time:
                filters['start_time'] = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
            if end_time:
                filters['end_time'] = datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")

            query = self.db.query(model)
            joins = {}

            for alias, path in field_mappings.items():
                relation, column_name = path.split('.')
                related_model = getattr(model, relation).property.mapper.class_
                joins[relation] = related_model
                query = query.add_columns(getattr(related_model, column_name).label(alias))

            for relation, related_model in joins.items():
                query = query.join(related_model, getattr(model, relation))

            if 'start_time' in filters:
                query = query.filter(model.created_at >= filters['start_time'])
            if 'end_time' in filters:
                query = query.filter(model.created_at <= filters['end_time'])

            for key, value in params.items():
                if key.startswith('%'):
                    raw_key = key[1:]
                    if raw_key in field_mappings:
                        relation, column_name = field_mappings[raw_key].split('.')
                        related_model = joins.get(relation)
                        if related_model:
                            column = getattr(related_model, column_name, None)
                            if column is not None:
                                query = query.filter(column.like(f"%{value}%"))
                    else:
                        column = getattr(model, raw_key, None)
                        if column is not None:
                            query = query.filter(column.like(f"%{value}%"))
                elif key not in ['_start', '_count', '_order', '_by', 'startTime', 'endTime', '_fields']:
                    column = getattr(model, key, None)
                    if column is not None:
                        query = query.filter(column == value)

            total = 0
            if not no_total:
                total_query = self.db.query(model)
                for relation, related_model in joins.items():
                    total_query = total_query.join(related_model, getattr(model, relation))
                if 'start_time' in filters:
                    total_query = total_query.filter(model.created_at >= filters['start_time'])
                if 'end_time' in filters:
                    total_query = total_query.filter(model.created_at <= filters['end_time'])
                total = total_query.count()

            if '_order' in params and '_by' in params:
                _order = params['_order']
                _by = params['_by']
                column = getattr(model, _by, None)
                if column is not None:
                    query = query.order_by(column.asc() if _order.lower() == 'asc' else column.desc())

            if '_start' in params and '_count' in params:
                query = query.offset(params['_start']).limit(params['_count'])

            result = query.all()

            if field_mappings:
                result_dict = [
                    {**row[0].to_dict(), **{alias: getattr(row, alias) for alias in field_mappings}}
                    for row in result
                ]
            else:
                result_dict = [item.to_dict() for item in result]

            return result_dict, total

        except Exception as e:
            raise ValueError(f"查询失败: {str(e)}") from e

    def insert_data(self, model, data):
        try:
            if 'id' not in data:
                data['id'] = str(uuid.uuid4())
            obj = model(**data)
            self.db.add(obj)
            self.db.commit()
            return obj
        except Exception as e:
            self.db.rollback()
            raise ValueError(f"插入失败: {str(e)}") from e

    def update_by_id(self, model, data):
        try:
            if 'id' not in data:
                raise ValueError("更新数据必须包含'id'")
            obj = self.db.query(model).filter(model.id == data['id']).first()
            if not obj:
                raise ValueError("未找到对应数据")
            for key, value in data.items():
                setattr(obj, key, value)
            self.db.commit()
            return obj
        except Exception as e:
            self.db.rollback()
            raise ValueError(f"更新失败: {str(e)}") from e

    def delete_by_conditions(self, model, filters: dict, safe_mode=True):
        try:
            query = self.db.query(model)
            for key, value in filters.items():
                column = getattr(model, key, None)
                if column is not None:
                    query = query.filter(column == value)

            if safe_mode and query.count() > 1:
                raise ValueError("匹配记录不唯一，删除操作被拒绝。")

            query.delete()
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise ValueError(f"删除失败: {str(e)}") from e
