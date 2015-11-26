from sqlalchemy import create_engine

SQL = "SELECT id, type FROM service WHERE enabled=1"

def conn(db_conn):
    try:
        db = create_engine(db_conn)
        services = db.execute(SQL)
    except Exception as e:
        print "Error at db connection"
        print e

    return services


def get_services(db_services):
    services = []
    for service in db_services:
        services.append(service)

    return services
