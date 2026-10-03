export type ValidationResult<T> =
  | { valid: true; value: T }
  | { valid: false; error: string };

export function validateCreateTask(input: unknown): ValidationResult<{ title: string }> {
  if (!input || typeof input !== 'object' || !('title' in input)) {
    return { valid: false, error: 'Title is required' };
  }

  const title = (input as { title?: unknown }).title;
  if (typeof title !== 'string' || title.trim().length === 0) {
    return { valid: false, error: 'Title is required' };
  }

  return { valid: true, value: { title: title.trim() } };
}

export function validateTaskUpdate(
  rawId: string,
  done: unknown,
): ValidationResult<{ id: number; done: boolean }> {
  const id = Number(rawId);
  if (!Number.isInteger(id) || typeof done !== 'boolean') {
    return {
      valid: false,
      error: 'A numeric id and boolean done value are required',
    };
  }

  return { valid: true, value: { id, done } };
}
