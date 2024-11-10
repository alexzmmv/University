#include "UserPlanner.h"
#include "Activity.h"

class htmlUserPlanner : public UserPlannerModel {
public:
    htmlUserPlanner();
    ~htmlUserPlanner();
    void addActivity(Activity& activity) override;
    void removeActivity(Activity& activity) override;

    [[maybe_unused]] void saveActivities(const std::string filePath);
};
