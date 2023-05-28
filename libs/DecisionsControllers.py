from _database.db import get_db
import calendar
import datetime
import uuid


def create_id():
    store_id = uuid.uuid4().hex
    return {"id": store_id}


def insert_item(table, year, month, day, file_name, date, text_list):
    db = get_db()
    cursor = db.cursor()
    statement = "INSERT INTO {}(year, month, day, file_name, date, text_list) VALUES (?, ?, ?, ?, ?, ?)".format(
        table)
    cursor.execute(statement, [year, month, day,
                   file_name, date, text_list])
    db.commit()
    return True


def update_item(table, id, year, month, day, file_name, date, text_list):
    db = get_db()
    cursor = db.cursor()
    statement = "UPDATE {} SET year = ?, month = ?, day = ?, file_name = ?, date = ?, text_list = ? WHERE id = ?".format(
        table)
    cursor.execute(statement, [year, month, day,
                   file_name, date, text_list, id])
    db.commit()
    return True


def delete_item(table, id):
    db = get_db()
    cursor = db.cursor()
    statement = "DELETE FROM {} WHERE id = ?".format(table)
    cursor.execute(statement, [id])
    db.commit()
    return True


def get_by_id(table, id):
    db = get_db()
    cursor = db.cursor()
    statement = "SELECT * FROM {} WHERE id = ?".format(table)
    cursor.execute(statement, [id])
    item = [
        dict(id=row[0], year=row[1], month=row[2], day=row[3],
             file_name=row[4], date=row[5], text_list=row[6])
        for row in cursor.fetchall()
    ]
    if item is not None:
        return item


def get_sumary_item(table, year, month, day):
    db = get_db()
    cursor = db.cursor()
    query = "SELECT id,date,file_name,text_list FROM {} WHERE year = ? AND month= ? AND day = ?".format(
        table)
    cursor.execute(query, [year, month, day])
    items = [
        dict(id=row[0], date=row[1], file_name=row[2], text_list=row[3])
        for row in cursor.fetchall()
    ]
    if items is not None:
        return items


def get_complete_item(table):
    db = get_db()
    cursor = db.cursor()
    query = "SELECT * FROM {} LIMIT 1000".format(table)
    cursor.execute(query)
    items = [
        dict(id=row[0], year=row[1], month=row[2], day=row[3],
             file_name=row[4], date=row[5], text_list=row[6])
        for row in cursor.fetchall()
    ]
    if items is not None:
        return items


def get_days_by_month(ActualYear, ActualMonth):
    days_name = [{"id": "0", "french_name": "Dimanche"}, {"id": "1", "french_name": "Lundi"}, {"id": "2", "french_name": "Mardi"}, {
        "id": "3", "french_name": "Mercredi"}, {"id": "4", "french_name": "Jeudi"}, {"id": "5", "french_name": "Vendredi"}, {"id": "6", "french_name": "Samedi"}]
    months_name = [{"id": "01", "french_name": "Janvier"}, {"id": "02", "french_name": "Février"}, {"id": "03", "french_name": "Mars"}, {"id": "04", "french_name": "Avril"}, {"id": "05", "french_name": "Mai"}, {"id": "06", "french_name": "Juin"}, {
        "id": "07", "french_name": "Juillet"}, {"id": "08", "french_name": "Août"}, {"id": "09", "french_name": "Septembre"}, {"id": "10", "french_name": "Octobre"}, {"id": "11", "french_name": "Novembre"}, {"id": "12", "french_name": "Décembre"}]
    now = datetime.datetime.now().date()
    cal = calendar.Calendar()
    listDateOfActualMonth = cal.monthdatescalendar(
        int(ActualYear), int(ActualMonth))
    reformatedDays = []

    for week in listDateOfActualMonth:
        for dayOfWeek in week:

            for day in days_name:
                if day["id"] == dayOfWeek.strftime("%w"):
                    actual_day = day["french_name"]
                    break

            for month in months_name:
                if month["id"] == dayOfWeek.strftime("%m"):
                    actual_month = month["french_name"]
                    break

            if int(ActualMonth) == int(dayOfWeek.strftime("%m")):
                builded_day = actual_day + " " + \
                    dayOfWeek.strftime("%d") + " " + actual_month + \
                    " " + dayOfWeek.strftime("%Y")
                if dayOfWeek <= now:
                    status = True
                else:
                    status = False
                reformatedDays.append(
                    {"day_name": builded_day, "active": status, "delta_days": int((now-dayOfWeek).days)})

    return reformatedDays


def get_delta_info(table):
    db = get_db()
    cursor = db.cursor()

    query = "SELECT DISTINCT year, month FROM {};".format(table)
    cursor.execute(query)
    items = [
        dict(year=row[0], month=row[1])
        for row in cursor.fetchall()
    ]
    if items is not None:
        return items
