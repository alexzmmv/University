#include "DataBaseRepo.h"
#include <stdexcept>

DataBaseRepo::DataBaseRepo(std::string dbPath)
{
    this->dbPath = dbPath;
    int rc = sqlite3_open(dbPath.c_str(), &this->db);
    if (rc)
        throw std::invalid_argument("Can't open database");
    char* zErrMsg = 0;
    const char* sql = "CREATE TABLE IF NOT EXISTS activities("  \
        "ID INTEGER PRIMARY KEY AUTOINCREMENT," \
        "TITLE TEXT NOT NULL," \
        "DESCRIPTION TEXT NOT NULL," \
        "LINK TEXT NOT NULL," \
        "YEAR INT NOT NULL," \
        "MONTH INT NOT NULL," \
        "DAY INT NOT NULL," \
        "HOUR INT NOT NULL," \
        "MINUTE INT NOT NULL," \
        "PEOPLE_NUMBER INT NOT NULL," \
        "DURATION INT NOT NULL);";
    rc = sqlite3_exec(this->db, sql, 0, 0, &zErrMsg);
    if (rc != SQLITE_OK)
    {
        std::string error = "SQL error: ";
        error += zErrMsg;
        sqlite3_free(zErrMsg);
        throw std::invalid_argument(error);
    }
    loadActivities();
}

void DataBaseRepo::loadActivities() {
    char *zErrMsg = 0;
    const char *sql = "SELECT * FROM activities;";
    sqlite3_stmt *stmt;
    int rc = sqlite3_prepare_v2(this->db, sql, -1, &stmt, 0);
    if (rc != SQLITE_OK) {
        std::string error = "SQL error: ";
        error += zErrMsg;
        sqlite3_free(zErrMsg);
        throw std::invalid_argument(error);
    }
    while (sqlite3_step(stmt) == SQLITE_ROW) {
        std::string title = std::string(reinterpret_cast<const char *>(sqlite3_column_text(stmt, 1)));
        std::string description = std::string(reinterpret_cast<const char *>(sqlite3_column_text(stmt, 2)));
        std::string link = std::string(reinterpret_cast<const char *>(sqlite3_column_text(stmt, 3)));
        DateTime dateTime = DateTime(sqlite3_column_int(stmt, 4), sqlite3_column_int(stmt, 5),
                                     sqlite3_column_int(stmt, 6), sqlite3_column_int(stmt, 7),
                                     sqlite3_column_int(stmt, 8));
        int peopleNumber = sqlite3_column_int(stmt, 9);
        int duration = sqlite3_column_int(stmt, 10);
        this->activities.push_back(new Activity(title, description, link, dateTime, peopleNumber, duration));
    }
    sqlite3_finalize(stmt);
}

DataBaseRepo::~DataBaseRepo()
{
    sqlite3_close(this->db);
}

void DataBaseRepo::addActivity(std::string title, std::string description, std::string link, DateTime dateTime, int peopleNumber, int duration)
{
    Repository::addActivity(title, description, link, dateTime, peopleNumber, duration);
    char* zErrMsg = 0;
    std::string sql = "INSERT INTO activities (TITLE, DESCRIPTION, LINK, YEAR, MONTH, DAY, HOUR, MINUTE, PEOPLE_NUMBER, DURATION) VALUES ('" + title + "', '" + description + "', '" + link + "', " + std::to_string(dateTime.getYear()) + ", " + std::to_string(dateTime.getMonth()) + ", " + std::to_string(dateTime.getDay()) + ", " + std::to_string(dateTime.getHour()) + ", " + std::to_string(dateTime.getMinute()) + ", " + std::to_string(peopleNumber) + ", " + std::to_string(duration) + ");";
    int rc = sqlite3_exec(this->db, sql.c_str(), 0, 0, &zErrMsg);
    if (rc != SQLITE_OK)
    {
        std::string error = "SQL error: ";
        error += zErrMsg;
        sqlite3_free(zErrMsg);
        throw std::invalid_argument(error);
    }
}

void DataBaseRepo::removeActivity(std::string title)
{
    Repository::removeActivity(title);
    char* zErrMsg = 0;
    std::string sql = "DELETE FROM activities WHERE TITLE = '" + title + "';";
    int rc = sqlite3_exec(this->db, sql.c_str(), 0, 0, &zErrMsg);
    if (rc != SQLITE_OK)
    {
        std::string error = "SQL error: ";
        error += zErrMsg;
        sqlite3_free(zErrMsg);
        throw std::invalid_argument(error);
    }
}

void DataBaseRepo::updateActivity(std::string title, std::string description, std::string link, DateTime dateTime, int peopleNumber, int duration)
{
    Repository::updateActivity(title, description, link, dateTime, peopleNumber, duration);
    char* zErrMsg = 0;
    std::string sql = "UPDATE activities SET DESCRIPTION = '" + description + "', LINK = '" + link + "', YEAR = " + std::to_string(dateTime.getYear()) + ", MONTH = " + std::to_string(dateTime.getMonth()) + ", DAY = " + std::to_string(dateTime.getDay()) + ", HOUR = " + std::to_string(dateTime.getHour()) + ", MINUTE = " + std::to_string(dateTime.getMinute()) + ", PEOPLE_NUMBER = " + std::to_string(peopleNumber) + ", DURATION = " + std::to_string(duration) + " WHERE TITLE = '" + title + "';";
    int rc = sqlite3_exec(this->db, sql.c_str(), 0, 0, &zErrMsg);
    if (rc != SQLITE_OK)
    {
        std::string error = "SQL error: ";
        error += zErrMsg;
        sqlite3_free(zErrMsg);
        throw std::invalid_argument(error);
    }
}
