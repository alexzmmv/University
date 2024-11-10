#pragma once

#include <QAbstractTableModel>
#include <vector>
#include "Activity.h"

class UserPlannerModelForGui : public QAbstractTableModel
{
Q_OBJECT
private:
    std::vector<Activity> activities;
    // 'title', 'description', 'link', 'peopleGoing', 'dateTime', 'duration'
public:
    explicit UserPlannerModelForGui(QObject* parent = nullptr);

    int rowCount(const QModelIndex& parent = QModelIndex()) const override;
    int columnCount(const QModelIndex& parent = QModelIndex()) const override;
    QVariant data(const QModelIndex& index, int role = Qt::DisplayRole) const override;
    QVariant headerData(int section, Qt::Orientation orientation, int role = Qt::DisplayRole) const override;

    void setActivities(const std::vector<Activity>& activities);
};
