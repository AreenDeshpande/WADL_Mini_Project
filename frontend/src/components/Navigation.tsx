import { useState } from "react";
import { Menu, X, Layout, FileText, User, BookOpen, Microscope, GitBranch, FileCheck, Map } from "lucide-react";
import { Link, useLocation } from "react-router-dom";
import { cn } from "@/lib/utils";

const Navigation = () => {
  const [isOpen, setIsOpen] = useState(false);
  const location = useLocation();

  const navItems = [
    { 
      name: "Dashboard", 
      path: "/dashboard", 
      icon: <Layout className="h-4 w-4" /> 
    },
    { 
      name: "Research Papers", 
      path: "/researchpaper", 
      icon: <Microscope className="h-4 w-4" /> 
    },
    { 
      name: "ATS Check", 
      path: "/ats", 
      icon: <FileCheck className="h-4 w-4" /> 
    },
    { 
      name: "GitHub Analyzer", 
      path: "/githubchat", 
      icon: <FileCheck className="h-4 w-4" /> 
    },
    { 
      name: "Notes", 
      path: "/notes", 
      icon: <FileText className="h-4 w-4" /> 
    },
    { 
      name: "Profile", 
      path: "/profile", 
      icon: <User className="h-4 w-4" /> 
    },
  ];

  return (
    <nav className="fixed top-0 w-full z-50 bg-black/80 backdrop-blur-sm border-b border-white/10">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          <div className="flex-shrink-0">
            <Link 
              to="/dashboard" 
              className="text-xl font-semibold text-white hover:text-purple-400 transition-colors flex items-center gap-2"
            >
              <BookOpen className="h-6 w-6" />
              CogniLearn
            </Link>
          </div>
          
          <div className="hidden md:block">
            <div className="ml-10 flex items-baseline space-x-4">
              {navItems.map((item) => (
                <Link
                  key={item.name}
                  to={item.path}
                  className={cn(
                    "px-3 py-2 rounded-md text-sm font-medium transition-all duration-200",
                    "hover:bg-purple-500/10 hover:text-purple-400 flex items-center gap-2",
                    location.pathname === item.path 
                      ? "bg-purple-500/20 text-purple-400" 
                      : "text-gray-300"
                  )}
                >
                  {item.icon}
                  {item.name}
                </Link>
              ))}
            </div>
          </div>
          
          <div className="md:hidden">
            <button
              onClick={() => setIsOpen(!isOpen)}
              className="inline-flex items-center justify-center p-2 rounded-md text-gray-300 hover:bg-purple-500/10 hover:text-purple-400 focus:outline-none"
              aria-label="Toggle menu"
            >
              {isOpen ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
            </button>
          </div>
        </div>
      </div>

      {/* Mobile menu */}
      {isOpen && (
        <div className="md:hidden">
          <div className="px-2 pt-2 pb-3 space-y-1 sm:px-3 bg-black/90 backdrop-blur-sm">
            {navItems.map((item) => (
              <Link
                key={item.name}
                to={item.path}
                className={cn(
                  "flex items-center gap-2 px-3 py-2 rounded-md text-base font-medium",
                  "hover:bg-purple-500/10 hover:text-purple-400 transition-all duration-200",
                  location.pathname === item.path 
                    ? "bg-purple-500/20 text-purple-400" 
                    : "text-gray-300"
                )}
                onClick={() => setIsOpen(false)}
              >
                {item.icon}
                {item.name}
              </Link>
            ))}
          </div>
        </div>
      )}
    </nav>
  );
};

export default Navigation;
