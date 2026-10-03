import { describe, expect, it } from 'vitest';
import { validateCreateTask, validateTaskUpdate } from '../../to-do-list/backend/src/validation';

describe('task validation', () => {
  it('accepts and trims a non-empty title', () => {
    expect(validateCreateTask({ title: '  Buy milk  ' })).toEqual({
      valid: true,
      value: { title: 'Buy milk' },
    });
  });

  it('rejects missing, empty, and non-string titles', () => {
    expect(validateCreateTask({})).toEqual({ valid: false, error: 'Title is required' });
    expect(validateCreateTask({ title: '   ' })).toEqual({ valid: false, error: 'Title is required' });
    expect(validateCreateTask({ title: 123 })).toEqual({ valid: false, error: 'Title is required' });
  });

  it('accepts numeric ids and boolean completion values', () => {
    expect(validateTaskUpdate('7', true)).toEqual({
      valid: true,
      value: { id: 7, done: true },
    });
  });

  it('rejects invalid ids and completion values', () => {
    expect(validateTaskUpdate('abc', true).valid).toBe(false);
    expect(validateTaskUpdate('7', 'true').valid).toBe(false);
  });
});
