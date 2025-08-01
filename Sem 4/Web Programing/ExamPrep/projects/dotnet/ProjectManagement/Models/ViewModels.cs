namespace ProjectManagement.Models
{
    public class DeveloperAssignmentViewModel
    {
        public string DeveloperName { get; set; } = string.Empty;
        public List<string> ProjectNames { get; set; } = new List<string>();
    }
    
    public class HomeViewModel
    {
        public string CurrentUserName { get; set; } = string.Empty;
        public List<Project> AllProjects { get; set; } = new List<Project>();
        public List<string> UserProjects { get; set; } = new List<string>();
        public List<SoftwareDeveloper> AllDevelopers { get; set; } = new List<SoftwareDeveloper>();
    }
}
