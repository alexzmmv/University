using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using Microsoft.AspNetCore.Authentication.JwtBearer;
using Microsoft.IdentityModel.Tokens;
using System.Text.Json.Serialization;
using System.Text;
using System.IdentityModel.Tokens.Jwt;
using System.Security.Claims;


var builder = WebApplication.CreateBuilder(args);

builder.Services.AddSwaggerGen(c =>
{
    
    // Configure Swagger to use Bearer authentication
    c.AddSecurityDefinition("Bearer", new Microsoft.OpenApi.Models.OpenApiSecurityScheme
    {
        Name = "Authorization",
        In = Microsoft.OpenApi.Models.ParameterLocation.Header,
        Type = Microsoft.OpenApi.Models.SecuritySchemeType.Http,
        Scheme = "Bearer",
        BearerFormat = "JWT",
        Description = "JWT Authorization header using the Bearer scheme. Enter 'Bearer' [space] and then your token in the text input below."
    });
    
    // Add security requirement for Bearer authentication on the API endpoints
    c.AddSecurityRequirement(new Microsoft.OpenApi.Models.OpenApiSecurityRequirement
    {
        {
            new Microsoft.OpenApi.Models.OpenApiSecurityScheme
            {
                Reference = new Microsoft.OpenApi.Models.OpenApiReference
                {
                    Type = Microsoft.OpenApi.Models.ReferenceType.SecurityScheme,
                    Id = "Bearer"
                }
            },
            Array.Empty<string>()
        }
    });
});

// Configure JWT
var jwtSettings = builder.Configuration.GetSection("JwtSettings");
var secretKey = jwtSettings["SecretKey"] ?? throw new InvalidOperationException("JWT SecretKey is not configured in appsettings.json");
var key = Encoding.ASCII.GetBytes(secretKey);

// Add authentication
builder.Services.AddAuthentication(options =>
{
    options.DefaultAuthenticateScheme = JwtBearerDefaults.AuthenticationScheme;
    options.DefaultChallengeScheme = JwtBearerDefaults.AuthenticationScheme;
})
.AddJwtBearer(options =>
{
    options.RequireHttpsMetadata = false;
    options.SaveToken = true;
    options.TokenValidationParameters = new TokenValidationParameters
    {
        ValidateIssuerSigningKey = true,
        IssuerSigningKey = new SymmetricSecurityKey(key),
        ValidateIssuer = false,
        ValidateAudience = false,
        ClockSkew = TimeSpan.Zero
    };
});

builder.Services.AddAuthorization();

builder.Services.AddDbContext<ApplicationDbContext>(options =>
    options.UseMySql(
        builder.Configuration.GetConnectionString("DefaultConnection"),
        ServerVersion.AutoDetect(builder.Configuration.GetConnectionString("DefaultConnection"))
    )
);

builder.Services.AddCors(options =>
{
    options.AddDefaultPolicy(policy =>
    {
        policy.AllowAnyOrigin()
              .AllowAnyMethod()
              .AllowAnyHeader();
    });
});

builder.Services.AddEndpointsApiExplorer();

var app = builder.Build();

// Add Swagger middleware BEFORE app.UseCors()
if (app.Environment.IsDevelopment() || true) // Enable in all environments for now
{
    app.UseSwagger();
    app.UseSwaggerUI(c =>
    {
        c.SwaggerEndpoint("/swagger/v1/swagger.json", "Vacation Destinations API v1");
        c.RoutePrefix = "swagger";
    });
}

app.UseCors();
app.UseAuthentication();
app.UseAuthorization();

// Public endpoints
app.MapGet("/", () => "Vacation Destinations API");
app.MapGet("/health", () => "OK");

// Authentication endpoints
app.MapPost("/api/v1/auth/register", async (ApplicationDbContext db, [FromBody] RegisterRequest request) =>
{
    if (string.IsNullOrEmpty(request.Username) || string.IsNullOrEmpty(request.Password))
    {
        return Results.BadRequest(new { error = "Username and password are required" });
    }

    if (request.Password.Length < 6)
    {
        return Results.BadRequest(new { error = "Password must be at least 6 characters long" });
    }

    // Check if user already exists
    var existingUser = await db.Users.FirstOrDefaultAsync(u => u.Username == request.Username);
    if (existingUser != null)
    {
        return Results.BadRequest(new { error = "Username already exists" });
    }

    // Create new user
    var hashedPassword = BCrypt.Net.BCrypt.HashPassword(request.Password);
    var user = new User
    {
        Username = request.Username,
        PasswordHash = hashedPassword,
        Email = request.Email,
        CreatedAt = DateTime.UtcNow
    };

    db.Users.Add(user);
    await db.SaveChangesAsync();

    return Results.Ok(new { message = "User registered successfully" });
});

app.MapPost("/api/v1/auth/login", async (ApplicationDbContext db, [FromBody] LoginRequest request) =>
{
    if (string.IsNullOrEmpty(request.Username) || string.IsNullOrEmpty(request.Password))
    {
        return Results.BadRequest(new { error = "Username and password are required" });
    }

    var user = await db.Users.FirstOrDefaultAsync(u => u.Username == request.Username);
    if (user == null || !BCrypt.Net.BCrypt.Verify(request.Password, user.PasswordHash))
    {
        return Results.Unauthorized();
    }

    // Generate JWT token
    var tokenHandler = new JwtSecurityTokenHandler();
    var tokenDescriptor = new SecurityTokenDescriptor
    {
        Subject = new ClaimsIdentity(new[]
        {
            new Claim(ClaimTypes.NameIdentifier, user.Id.ToString()),
            new Claim(ClaimTypes.Name, user.Username)
        }),
        Expires = DateTime.UtcNow.AddMinutes(60), // Token valid for 60 minutes
        SigningCredentials = new SigningCredentials(new SymmetricSecurityKey(key), SecurityAlgorithms.HmacSha256Signature)
    };

    var token = tokenHandler.CreateToken(tokenDescriptor);
    var tokenString = tokenHandler.WriteToken(token);

    return Results.Ok(new
    {
        token = tokenString,
        user = new
        {
            id = user.Id,
            username = user.Username,
            email = user.Email
        }
    });
});

// Protected endpoints - Countries
app.MapGet("/api/v1/countries", async (ApplicationDbContext db, [FromQuery] bool with_destinations = false) =>
{
    if (with_destinations)
    {
        var countries = await db.Countries
            .Where(c => c.Destinations.Any())
            .OrderBy(c => c.Name)
            .ToListAsync();
        return Results.Ok(new { countries });
    }
    else
    {
        var countries = await db.Countries
            .OrderBy(c => c.Name)
            .ToListAsync();
        return Results.Ok(new { countries });
    }
}).RequireAuthorization();

app.MapGet("/api/v1/countries/{id:int}", async (ApplicationDbContext db, int id) =>
{
    var country = await db.Countries.FindAsync(id);
    
    if (country == null)
        return Results.NotFound(new { error = "Country not found" });
    
    return Results.Ok(country);
}).RequireAuthorization();

// Protected endpoints - Destinations
app.MapGet("/api/v1/destinations/cost-range", async (ApplicationDbContext db) =>
{
    var minCost = await db.Destinations.MinAsync(d => (float?)d.CostPerDay) ?? 0;
    var maxCost = await db.Destinations.MaxAsync(d => (float?)d.CostPerDay) ?? 10000000;
    
    return Results.Ok(new
    {
        min_cost = minCost,
        max_cost = maxCost
    });
}).RequireAuthorization();

app.MapGet("/api/v1/destinations/{id:int}", async (ApplicationDbContext db, int id) =>
{
    var destination = await db.Destinations
        .Include(d => d.Country)
        .Where(d => d.Id == id)
        .Select(d => new
        {
            d.Id,
            d.Name,
            d.CountryId,
            country_name = d.Country.Name,
            d.Description,
            d.TouristTargets,
            d.CostPerDay,
            d.CreatedAt
        })
        .FirstOrDefaultAsync();
    
    if (destination == null)
        return Results.NotFound(new { error = "Destination not found" });
    
    return Results.Ok(destination);
}).RequireAuthorization();

app.MapPost("/api/v1/destinations", async (ApplicationDbContext db, [FromBody] DestinationRequest request) =>
{
    if (string.IsNullOrEmpty(request.Name) || string.IsNullOrEmpty(request.Country) || request.CostPerDay <= 0)
    {
        return Results.BadRequest(new { error = "Name, country, and cost per day are required fields. Cost per day must be positive." });
    }
    
    var country = await db.Countries.FirstOrDefaultAsync(c => c.Name == request.Country);
    if (country == null)
    {
        country = new Country { Name = request.Country };
        db.Countries.Add(country);
        await db.SaveChangesAsync();
    }
    
    var newDestination = new Destination
    {
        Name = request.Name,
        CountryId = country.Id,
        Description = request.Description,
        TouristTargets = request.TouristTargets,
        CostPerDay = request.CostPerDay,
        CreatedAt = DateTime.UtcNow
    };
    
    db.Destinations.Add(newDestination);
    await db.SaveChangesAsync();
    
    var createdDestination = await db.Destinations
        .Include(d => d.Country)
        .Where(d => d.Id == newDestination.Id)
        .Select(d => new
        {
            d.Id,
            d.Name,
            d.CountryId,
            country_name = d.Country.Name,
            d.Description,
            d.TouristTargets,
            d.CostPerDay,
            d.CreatedAt
        })
        .FirstAsync();
    
    return Results.Created($"/api/v1/destinations/{newDestination.Id}", new
    {
        message = "Destination created successfully",
        destination = createdDestination
    });
}).RequireAuthorization();

app.MapPut("/api/v1/destinations/{id:int}", async (ApplicationDbContext db, int id, DestinationRequest request) =>
{
    var destination = await db.Destinations.FindAsync(id);
    if (destination == null)
        return Results.NotFound(new { error = "Destination not found" });
    
    if (string.IsNullOrEmpty(request.Name) || string.IsNullOrEmpty(request.Country) || request.CostPerDay <= 0)
    {
        return Results.BadRequest(new { error = "Name, country, and cost per day are required fields. Cost per day must be positive." });
    }
    
    var country = await db.Countries.FirstOrDefaultAsync(c => c.Name == request.Country);
    if (country == null)
    {
        country = new Country { Name = request.Country };
        db.Countries.Add(country);
        await db.SaveChangesAsync();
    }
    
    destination.Name = request.Name;
    destination.CountryId = country.Id;
    destination.Description = request.Description;
    destination.TouristTargets = request.TouristTargets;
    destination.CostPerDay = request.CostPerDay;
    
    await db.SaveChangesAsync();
    
    var updatedDestination = await db.Destinations
        .Include(d => d.Country)
        .Where(d => d.Id == id)
        .Select(d => new
        {
            d.Id,
            d.Name,
            d.CountryId,
            country_name = d.Country.Name,
            d.Description,
            d.TouristTargets,
            d.CostPerDay,
            d.CreatedAt
        })
        .FirstAsync();
    
    return Results.Ok(new
    {
        message = "Destination updated successfully",
        destination = updatedDestination
    });
}).RequireAuthorization();

app.MapDelete("/api/v1/destinations/{id:int}", async (ApplicationDbContext db, int id) =>
{
    var destination = await db.Destinations.FindAsync(id);
    if (destination == null)
        return Results.NotFound(new { error = "Destination not found" });
    
    db.Destinations.Remove(destination);
    await db.SaveChangesAsync();
    
    return Results.Ok(new { message = "Destination deleted successfully" });
}).RequireAuthorization();

app.MapGet("/api/v1/destinations/count", async (ApplicationDbContext db) =>
{
    var count = await db.Destinations.CountAsync();
    return Results.Ok(new { total = count });
}).RequireAuthorization();

app.MapGet("/api/v1/destinations", async (
    ApplicationDbContext db,
    [FromQuery] int? id = null,
    [FromQuery] string? action = null,
    [FromQuery] int page = 1,
    [FromQuery] int limit = 10,
    [FromQuery] string? countries = null,
    [FromQuery] float? min_cost = null,
    [FromQuery] float? max_cost = null,
    [FromQuery] string? search = null) =>
{
    // Validate pagination parameters
    if (page < 1)
        return Results.BadRequest(new { error = "Page must be greater than 0" });
    if (limit < 1 || limit > 100)
        return Results.BadRequest(new { error = "Limit must be between 1 and 100" });
    // Validate cost range parameters
    if (min_cost.HasValue && min_cost < 0)
        return Results.BadRequest(new { error = "Minimum cost cannot be negative" });
    if (max_cost.HasValue && max_cost < 0)
        return Results.BadRequest(new { error = "Maximum cost cannot be negative" });
    if (min_cost.HasValue && max_cost.HasValue && min_cost > max_cost)
        return Results.BadRequest(new { error = "Minimum cost cannot be greater than maximum cost" });

    if (action == "cost-range")
    {
        var minCost = await db.Destinations.MinAsync(d => (float?)d.CostPerDay) ?? 0;
        var maxCost = await db.Destinations.MaxAsync(d => (float?)d.CostPerDay) ?? 10000000;

        return Results.Ok(new
        {
            min_cost = minCost,
            max_cost = maxCost
        });
    }
    
    // If id is provided, return a single destination
    if (id.HasValue)
    {
        var destination = await db.Destinations
            .Include(d => d.Country)
            .Where(d => d.Id == id.Value)
            .Select(d => new
            {
                d.Id,
                d.Name,
                d.CountryId,
                country_name = d.Country.Name,
                d.Description,
                tourist_targets = d.TouristTargets,
                cost_per_day = d.CostPerDay,
                d.CreatedAt
            })
            .FirstOrDefaultAsync();

        if (destination == null)
            return Results.NotFound(new { error = "Destination not found" });

        return Results.Ok(destination);
    }
    
    var query = db.Destinations
        .Include(d => d.Country)
        .AsQueryable();    if (!string.IsNullOrEmpty(countries))
    {
        var countryIds = countries.Split(',', StringSplitOptions.RemoveEmptyEntries)
            .Select(s => int.Parse(s.Trim()))
            .ToList();

        if (countryIds.Count == 1)
        {
            var singleId = countryIds[0];
            query = query.Where(d => d.CountryId == singleId);
        }
        else if (countryIds.Count > 1)
        {
            var firstId = countryIds[0];
            var predicate = query.Where(d => d.CountryId == firstId);
            
            foreach (var countryId in countryIds.Skip(1))
            {
                var currentId = countryId;
                predicate = predicate.Union(query.Where(d => d.CountryId == currentId));
            }
            
            query = predicate;
        }
    }

    // Apply cost range filters
    if (min_cost.HasValue)
    {
        query = query.Where(d => d.CostPerDay >= min_cost.Value);
    }
    
    if (max_cost.HasValue)
    {
        query = query.Where(d => d.CostPerDay <= max_cost.Value);
    }
    
    if (!string.IsNullOrEmpty(search))
    {
        query = query.Where(d => 
            d.Name.Contains(search) || 
            d.Description.Contains(search) || 
            d.Country.Name.Contains(search));
    }
    
    var totalItems = await query.CountAsync();
    var totalPages = (int)Math.Ceiling(totalItems / (double)limit);
    var currentPage = Math.Max(1, Math.Min(page, totalPages > 0 ? totalPages : 1));
    var offset = (currentPage - 1) * limit;
    
    var destinations = await query
        .OrderBy(d => d.Name)
        .Skip(offset)
        .Take(limit)
        .Select(d => new
        {
            d.Id,
            d.Name,
            d.CountryId,
            country_name = d.Country.Name,
            d.Description,
            tourist_targets = d.TouristTargets,
            cost_per_day = d.CostPerDay,
            d.CreatedAt
        })
        .ToListAsync();
    
    var filters = new 
    {
        countries = !string.IsNullOrEmpty(countries) ? 
            countries.Split(',', StringSplitOptions.RemoveEmptyEntries)
                .Where(s => !string.IsNullOrWhiteSpace(s) && int.TryParse(s.Trim(), out _))
                .Select(s => int.Parse(s.Trim()))
                .ToList() : 
            new List<int>(),
        min_cost,
        max_cost,
        search
    };
    
    return Results.Ok(new
    {
        destinations,
        pagination = new
        {
            currentPage,
            totalPages,
            totalItems,
            itemsPerPage = limit
        },
        filters
    });
}).RequireAuthorization();

app.Run();


// Models
public class User
{
    public int Id { get; set; }
    public string Username { get; set; } = string.Empty;
    public string PasswordHash { get; set; } = string.Empty;
    public string Email { get; set; } = string.Empty;
    public DateTime CreatedAt { get; set; } = DateTime.UtcNow;
}

public class Country
{
    public int Id { get; set; }
    public string Name { get; set; } = string.Empty;

    public ICollection<Destination> Destinations { get; set; } = new List<Destination>();
}

public class Destination
{
    public int Id { get; set; }
    public string Name { get; set; } = string.Empty;
    public int CountryId { get; set; }
    public string Description { get; set; } = string.Empty;
    public string TouristTargets { get; set; } = string.Empty;
    public float CostPerDay { get; set; }
    public DateTime CreatedAt { get; set; } = DateTime.UtcNow;
    
    public Country Country { get; set; } = null!;
}

// Request models
public class LoginRequest
{
    public string Username { get; set; } = string.Empty;
    public string Password { get; set; } = string.Empty;
}

public class RegisterRequest
{
    public string Username { get; set; } = string.Empty;
    public string Password { get; set; } = string.Empty;
    public string Email { get; set; } = string.Empty;
}

public class DestinationRequest
{
    public string Name { get; set; } = string.Empty;
    public string Country { get; set; } = string.Empty;
    public string Description { get; set; } = string.Empty;
    
    private string? _touristTargets;
    
    public string TouristTargets 
    { 
        get => _touristTargets ?? string.Empty; 
        set => _touristTargets = value; 
    }
    
    [JsonPropertyName("tourist_targets")]
    public string? TouristTargetsAlt 
    { 
        get => _touristTargets; 
        set 
        { 
            if (value != null)
                _touristTargets = value; 
        } 
    }
    
    private float _costPerDay;
    
    public float CostPerDay 
    { 
        get => _costPerDay; 
        set => _costPerDay = value; 
    }
    
    [JsonPropertyName("cost_per_day")]
    public float? CostPerDayAlt 
    { 
        get => _costPerDay; 
        set 
        { 
            if (value.HasValue)
                _costPerDay = value.Value; 
        } 
    }
}

public class ApplicationDbContext : DbContext
{
    public ApplicationDbContext(DbContextOptions<ApplicationDbContext> options)
        : base(options)
    {
    }
    
    public DbSet<User> Users { get; set; } = null!;
    public DbSet<Country> Countries { get; set; } = null!;
    public DbSet<Destination> Destinations { get; set; } = null!;
    
    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        base.OnModelCreating(modelBuilder);
        
        modelBuilder.Entity<User>(entity =>
        {
            entity.HasKey(e => e.Id);
            entity.Property(e => e.Username).IsRequired();
            entity.HasIndex(e => e.Username).IsUnique();
            entity.Property(e => e.PasswordHash).IsRequired();
        });
        
        modelBuilder.Entity<Country>(entity =>
        {
            entity.HasKey(e => e.Id);
            entity.Property(e => e.Name).IsRequired();
            entity.HasIndex(e => e.Name).IsUnique();
        });
        
        modelBuilder.Entity<Destination>(entity =>
        {
            entity.HasKey(e => e.Id);
            entity.Property(e => e.Name).IsRequired();
            entity.Property(e => e.CostPerDay).IsRequired();
            
            entity.HasOne(d => d.Country)
                .WithMany(c => c.Destinations)
                .HasForeignKey(d => d.CountryId)
                .OnDelete(DeleteBehavior.Cascade);
        });
    }
}