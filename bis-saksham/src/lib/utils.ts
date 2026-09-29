import { type ClassValue, clsx } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export function formatDate(dateString: string): string {
  try {
    return new Date(dateString).toLocaleDateString("en-IN", {
      day: "numeric",
      month: "short",
      year: "numeric",
    });
  } catch {
    return dateString;
  }
}

export function getStatusColor(status: string): string {
  switch (status) {
    case "SATISFIED":
    case "COMPLETED":
    case "CONFIRMED":
      return "text-green-700 bg-green-50 border-green-200";
    case "MISSING":
    case "NOT_STARTED":
      return "text-red-700 bg-red-50 border-red-200";
    case "REVIEW":
    case "IN_PROGRESS":
    case "NEEDS_VERIFICATION":
      return "text-amber-700 bg-amber-50 border-amber-200";
    case "NOT_APPLICABLE":
    case "NO_REQUIREMENT":
      return "text-gray-600 bg-gray-50 border-gray-200";
    case "POTENTIALLY_APPLICABLE":
      return "text-indigo-700 bg-indigo-50 border-indigo-200";
    default:
      return "text-gray-600 bg-gray-50 border-gray-200";
  }
}

export function getStatusLabel(status: string): string {
  switch (status) {
    case "SATISFIED": return "Satisfied";
    case "MISSING": return "Missing";
    case "REVIEW": return "Needs Review";
    case "NOT_APPLICABLE": return "Not Applicable";
    case "COMPLETED": return "Completed";
    case "IN_PROGRESS": return "In Progress";
    case "NOT_STARTED": return "Not Started";
    case "CONFIRMED": return "Confirmed";
    case "POTENTIALLY_APPLICABLE": return "Potentially Applicable";
    case "NO_REQUIREMENT": return "No Requirement";
    case "NEEDS_VERIFICATION": return "Needs Verification";
    default: return status;
  }
}

export function getImpactColor(impact: string): string {
  switch (impact) {
    case "HIGH": return "text-red-700 bg-red-50 border-red-200";
    case "MEDIUM": return "text-amber-700 bg-amber-50 border-amber-200";
    case "LOW": return "text-green-700 bg-green-50 border-green-200";
    default: return "text-gray-600 bg-gray-50 border-gray-200";
  }
}
