using System.ComponentModel.DataAnnotations;

namespace ProjectManagement.Models
{
    public class SoftwareDeveloper
    {
        public int Id { get; set; }
        
        [Required]
        [StringLength(100)]
        public string Name { get; set; } = string.Empty;
        
        public int Age { get; set; }
        
        [StringLength(500)]
        public string Skills { get; set; } = string.Empty;
        
        // Navigation property for projects managed by this developer
        public virtual ICollection<Project> ManagedProjects { get; set; } = new List<Project>();
    }
}
