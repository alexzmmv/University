using Microsoft.EntityFrameworkCore;
using ProjectManagement.Models;

namespace ProjectManagement.Data
{
    public class ProjectManagementContext : DbContext
    {
        public ProjectManagementContext(DbContextOptions<ProjectManagementContext> options)
            : base(options)
        {
        }

        public DbSet<SoftwareDeveloper> SoftwareDevelopers { get; set; }
        public DbSet<Project> Projects { get; set; }

        protected override void OnModelCreating(ModelBuilder modelBuilder)
        {
            base.OnModelCreating(modelBuilder);

            // Configure SoftwareDeveloper entity
            modelBuilder.Entity<SoftwareDeveloper>(entity =>
            {
                entity.HasKey(e => e.Id);
                entity.Property(e => e.Name).IsRequired().HasMaxLength(100);
                entity.Property(e => e.Skills).HasMaxLength(500);
            });

            // Configure Project entity
            modelBuilder.Entity<Project>(entity =>
            {
                entity.HasKey(e => e.Id);
                entity.Property(e => e.Name).IsRequired().HasMaxLength(200);
                entity.Property(e => e.Description).HasMaxLength(1000);
                entity.Property(e => e.Members).HasMaxLength(2000);
                
                // Foreign key relationship
                entity.HasOne(p => p.ProjectManager)
                      .WithMany(d => d.ManagedProjects)
                      .HasForeignKey(p => p.ProjectManagerID)
                      .OnDelete(DeleteBehavior.SetNull);
            });

            // Seed data
            modelBuilder.Entity<SoftwareDeveloper>().HasData(
                new SoftwareDeveloper { Id = 1, Name = "John Smith", Age = 30, Skills = "Java, C#, Python" },
                new SoftwareDeveloper { Id = 2, Name = "Sarah Johnson", Age = 28, Skills = "JavaScript, React, Node.js" },
                new SoftwareDeveloper { Id = 3, Name = "Mike Davis", Age = 35, Skills = "C++, Java, MySQL" },
                new SoftwareDeveloper { Id = 4, Name = "Lisa Wilson", Age = 32, Skills = "Python, Django, PostgreSQL" },
                new SoftwareDeveloper { Id = 5, Name = "Tom Brown", Age = 29, Skills = "C#, ASP.NET, SQL Server" }
            );

            modelBuilder.Entity<Project>().HasData(
                new Project { Id = 1, ProjectManagerID = 1, Name = "E-Commerce Platform", Description = "Online shopping website", Members = "John Smith, Sarah Johnson, Mike Davis" },
                new Project { Id = 2, ProjectManagerID = 2, Name = "Mobile Banking App", Description = "iOS and Android banking application", Members = "Sarah Johnson, Lisa Wilson" },
                new Project { Id = 3, ProjectManagerID = 3, Name = "Data Analytics Dashboard", Description = "Business intelligence dashboard", Members = "Mike Davis, Tom Brown, Lisa Wilson" },
                new Project { Id = 4, ProjectManagerID = 1, Name = "Social Media API", Description = "RESTful API for social media platform", Members = "John Smith, Tom Brown" }
            );
        }
    }
}
