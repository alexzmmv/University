using System.Diagnostics;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using ProjectManagement.Data;
using ProjectManagement.Models;

namespace ProjectManagement.Controllers;

public class HomeController : Controller
{
    private readonly ILogger<HomeController> _logger;
    private readonly ProjectManagementContext _context;

    public HomeController(ILogger<HomeController> logger, ProjectManagementContext context)
    {
        _logger = logger;
        _context = context;
    }

    public async Task<IActionResult> Index(string userName = "")
    {
        var viewModel = new HomeViewModel
        {
            CurrentUserName = userName,
            AllProjects = await _context.Projects
                .Include(p => p.ProjectManager)
                .ToListAsync(),
            AllDevelopers = await _context.SoftwareDevelopers.ToListAsync()
        };        // Get user's projects if username is provided
        if (!string.IsNullOrEmpty(userName))
        {
            viewModel.UserProjects = await _context.Projects
                .Where(p => !string.IsNullOrEmpty(p.Members) && 
                           (p.Members == userName || 
                            p.Members.StartsWith(userName + ",") || 
                            p.Members.Contains(", " + userName + ",") || 
                            p.Members.EndsWith(", " + userName)))
                .Select(p => p.Name)
                .ToListAsync();
        }

        return View(viewModel);
    }    [HttpPost]
    public IActionResult SetUser(string userName)
    {
        return RedirectToAction("Index", new { userName });
    }[HttpPost]
    public async Task<IActionResult> AssignDeveloper(string developerName, string projectNames)
    {
        if (string.IsNullOrEmpty(developerName) || string.IsNullOrEmpty(projectNames))
        {
            TempData["Error"] = "Please provide both developer name and project names.";
            return RedirectToAction("Index");
        }

        // Parse project names from textarea (split by new lines)
        var projectNamesList = projectNames
            .Split(new[] { '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries)
            .Select(name => name.Trim())
            .Where(name => !string.IsNullOrEmpty(name))
            .ToList();

        if (!projectNamesList.Any())
        {
            TempData["Error"] = "Please provide at least one project name.";
            return RedirectToAction("Index");
        }

        // Check if developer exists
        var developer = await _context.SoftwareDevelopers
            .FirstOrDefaultAsync(d => d.Name.ToLower() == developerName.ToLower());

        if (developer == null)
        {
            TempData["Error"] = "Developer does not exist in the database. No assignments were made.";
            return RedirectToAction("Index");
        }

        int projectsAssigned = 0;
        int projectsCreated = 0;

        foreach (var projectName in projectNamesList)
        {
            var project = await _context.Projects
                .FirstOrDefaultAsync(p => p.Name.ToLower() == projectName.ToLower());

            if (project == null)
            {
                // Create new project with only the name
                project = new Project
                {
                    Name = projectName,
                    Description = "",
                    Members = developerName,
                    ProjectManagerID = null
                };
                _context.Projects.Add(project);
                projectsCreated++;
                projectsAssigned++;
            }
            else
            {
                // Add developer to existing project if not already a member
                var currentMembers = project.Members?.Split(',').Select(m => m.Trim().ToLower()).ToList() ?? new List<string>();
                
                if (!currentMembers.Contains(developerName.ToLower()))
                {
                    if (string.IsNullOrEmpty(project.Members))
                    {
                        project.Members = developerName;
                    }
                    else
                    {
                        project.Members += ", " + developerName;
                    }
                    projectsAssigned++;
                }
            }
        }

        await _context.SaveChangesAsync();
        
        string successMessage = $"Developer {developerName} has been assigned to {projectsAssigned} project(s).";
        if (projectsCreated > 0)
        {
            successMessage += $" {projectsCreated} new project(s) were created.";
        }
        
        TempData["Success"] = successMessage;

        return RedirectToAction("Index");
    }

    [HttpGet]
    public async Task<IActionResult> GetDevelopers()
    {
        var developers = await _context.SoftwareDevelopers.ToListAsync();
        return Json(developers);
    }

    public IActionResult Privacy()
    {
        return View();
    }

    [ResponseCache(Duration = 0, Location = ResponseCacheLocation.None, NoStore = true)]
    public IActionResult Error()
    {
        return View(new ErrorViewModel { RequestId = Activity.Current?.Id ?? HttpContext.TraceIdentifier });
    }
}
