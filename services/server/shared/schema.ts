import { z } from "zod";

/**
 * @file This file contains the Zod schemas for validating data related to educational resources.
 */
import { z } from "zod";

// Resource schema
/**
 * The Zod schema for an educational resource.
 */
export const resourceSchema = z.object({
  id: z.string(),
  title: z.string(),
  description: z.string(),
  skillLevel: z.enum(["beginner", "intermediate", "advanced"]),
  category: z.enum(["programming", "design", "marketing", "data-science"]),
  resourceType: z.enum(["video", "article", "course", "tutorial"]),
  duration: z.string(),
  imageUrl: z.string(),
  featured: z.boolean().default(false),
  createdAt: z.date().default(() => new Date()),
});

/**
 * The type for an educational resource.
 */
export type Resource = z.infer<typeof resourceSchema>;

// Insert schema (for creating new resources)
/**
 * The Zod schema for inserting a new educational resource.
 */
export const insertResourceSchema = resourceSchema.omit({
  id: true,
  createdAt: true,
});

/**
 * The type for inserting a new educational resource.
 */
export type InsertResource = z.infer<typeof insertResourceSchema>;

// Query filters schema
/**
 * The Zod schema for resource query filters.
 */
export const resourceFiltersSchema = z.object({
  search: z.string().optional(),
  skillLevel: z.enum(["beginner", "intermediate", "advanced"]).optional(),
  category: z.enum(["programming", "design", "marketing", "data-science"]).optional(),
  resourceType: z.enum(["video", "article", "course", "tutorial"]).optional(),
  page: z.number().int().positive().default(1),
  limit: z.number().int().positive().max(50).default(12),
});

/**
 * The type for resource query filters.
 */
export type ResourceFilters = z.infer<typeof resourceFiltersSchema>;

// Response schema for paginated resources
/**
 * The Zod schema for the response of paginated resources.
 */
export const resourcesResponseSchema = z.object({
  resources: z.array(resourceSchema),
  totalCount: z.number(),
  totalPages: z.number(),
  currentPage: z.number(),
  hasNextPage: z.boolean(),
  hasPrevPage: z.boolean(),
});

/**
 * The type for the response of paginated resources.
 */
export type ResourcesResponse = z.infer<typeof resourcesResponseSchema>;
