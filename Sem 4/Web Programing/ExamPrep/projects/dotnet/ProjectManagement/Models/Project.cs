using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace ProjectManagement.Models
{
    public class Project
    {
        public int Id { get; set; }
        
        [ForeignKey("ProjectManager")]
        public int? ProjectManagerID { get; set; }
        
        [Required]
        [StringLength(200)]
        public string Name { get; set; } = string.Empty;
        
        [StringLength(1000)]
        public string Description { get; set; } = string.Empty;
        
        [StringLength(2000)]
        public string Members { get; set; } = string.Empty; // Comma-separated list of member names
        
        // Navigation property
        public virtual SoftwareDeveloper? ProjectManager { get; set; }
    }
}
