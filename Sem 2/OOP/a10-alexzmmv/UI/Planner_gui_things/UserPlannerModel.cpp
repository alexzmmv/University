#include "UserPlannerModelForGui.h"

UserPlannerModelForGui::UserPlannerModelForGui(QObject* parent)
        : QAbstractTableModel(parent) {
}

int UserPlannerModelForGui::rowCount(const QModelIndex& parent) const {
    return parent.isValid() ? 0 : activities.size();
}

int UserPlannerModelForGui::columnCount(const QModelIndex& parent) const {
    return parent.isValid() ? 0 : 6;
}

QVariant UserPlannerModelForGui::data(const QModelIndex& index, int role) const {
    if (!index.isValid() || role != Qt::DisplayRole)
        return QVariant();

    Activity activity = activities[index.row()];
    switch (index.column()) {
        case 0:
            return QString::fromStdString(activity.getTitle());
        case 1:
            return QString::fromStdString(activity.getDescription());
        case 2:
            return QString::fromStdString(activity.getLink());
        case 3:
            return activity.getPeopleGoing();
        case 4:
            return QString::fromStdString(activity.getDateTime().toString());
        case 5:
            return activity.getDuration();
        default:
            return QVariant();
    }
}

QVariant UserPlannerModelForGui::headerData(int section, Qt::Orientation orientation, int role) const {
    if (role != Qt::DisplayRole)
        return QVariant();

    if (orientation == Qt::Horizontal) {
        switch (section) {
            case 0:
                return QString("Title");
            case 1:
                return QString("Description");
            case 2:
                return QString("Link");
            case 3:
                return QString("People Going");
            case 4:
                return QString("Date & Time");
            case 5:
                return QString("Duration");
            default:
                return QVariant();
        }
    }
    return QVariant();
}

void UserPlannerModelForGui::setActivities(const std::vector<Activity>& activities) {
    beginResetModel();
    this->activities = activities;
    endResetModel();
}
