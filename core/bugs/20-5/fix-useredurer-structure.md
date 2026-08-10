# Deep Dive: Type-Safe Reducer Actions in TypeScript (Unions vs. Enums)

When typing a `useReducer` in TypeScript, the structure of your `Action` type is the most critical factor for type safety. 

If you use a generic action structure like this (a common anti-pattern):
```typescript
// ❌ UNSAFE: Loose types
interface Action {
  type: string;
  payload?: any;
}
```
You completely lose type safety:
1. You can write typos in `action.type`.
2. Inside the reducer, `action.payload` is `any`, meaning you can access properties that don't exist, leading to runtime errors.
3. You can dispatch actions with mismatched payloads (e.g., sending an ID instead of a full item object).

Below is the comparison and implementation details of using **Discriminated Unions** vs. **Enums** to make your reducer 100% type-safe.

---

## Approach 1: Discriminated Unions (The Industry Standard & Recommended)

A **Discriminated Union** uses literal types as a "discriminator" (the `type` field) to link specific action types to their precise payload shapes.

### The Code
```typescript
interface CartItem {
  id: string;
  name: string;
  price: number;
}

// 1. Define distinct types for each action
type AddItemAction = {
  type: 'ADD_ITEM';
  payload: { item: CartItem; quantity: number };
};

type RemoveItemAction = {
  type: 'REMOVE_ITEM';
  payload: { id: string };
};

type ClearCartAction = {
  type: 'CLEAR_CART';
  // Note: No payload field is defined here, which means payload is illegal on CLEAR_CART!
};

// 2. Union them together
export type CartAction = AddItemAction | RemoveItemAction | ClearCartAction;
```

### Why this is 100% Type Safe in the Reducer:
TypeScript understands the `type` discriminator. Inside your `switch` block, as soon as you enter a `case`, TypeScript **narrows** the type of the action.

```typescript
function cartReducer(state: CartState, action: CartAction) {
  switch (action.type) {
    case 'ADD_ITEM':
      // Inside this block, action is automatically narrowed to AddItemAction!
      // TypeScript knows exactly that:
      // - action.payload is defined
      // - action.payload.item is of type CartItem
      // - action.payload.quantity is of type number
      return {
        ...state,
        items: [...state.items, action.payload.item] // Full autocomplete & safety!
      };

    case 'REMOVE_ITEM':
      // action is narrowed to RemoveItemAction
      // Trying to access action.payload.item here will cause a COMPILE error!
      return {
        ...state,
        items: state.items.filter(item => item.id !== action.payload.id)
      };

    case 'CLEAR_CART':
      // action is narrowed to ClearCartAction (no payload)
      // Trying to read action.payload here will cause a COMPILE error!
      return {
        ...state,
        items: []
      };
  }
}
```

---

## Approach 2: Enums + Discriminated Unions (The Hybrid Pattern)

If you prefer to avoid hardcoded string literals like `'ADD_ITEM'`, you can use a TypeScript `enum` for the action types, but **you must still combine it with a Discriminated Union** to keep payload type safety.

### The Code
```typescript
interface CartItem {
  id: string;
  name: string;
  price: number;
}

// 1. Declare the Enum
export enum CartActionType {
  ADD_ITEM = 'ADD_ITEM',
  REMOVE_ITEM = 'REMOVE_ITEM',
  CLEAR_CART = 'CLEAR_CART',
}

// 2. Map the Enum members to their payload shapes in a Discriminated Union
export type CartAction =
  | { type: CartActionType.ADD_ITEM; payload: { item: CartItem; quantity: number } }
  | { type: CartActionType.REMOVE_ITEM; payload: { id: string } }
  | { type: CartActionType.CLEAR_CART }; // No payload allowed
```

### Why this is 100% Type Safe in the Reducer:
Just like Approach 1, TypeScript narrows the type of `action` inside each `case` statement, but you reference the Enum keys instead of string literals:

```typescript
function cartReducer(state: CartState, action: CartAction) {
  switch (action.type) {
    case CartActionType.ADD_ITEM:
      // action is narrowed to: { type: CartActionType.ADD_ITEM; payload: { item: CartItem; quantity: number } }
      console.log(action.payload.item.name); // Safe!
      return state;

    case CartActionType.REMOVE_ITEM:
      // action is narrowed to: { type: CartActionType.REMOVE_ITEM; payload: { id: string } }
      console.log(action.payload.id); // Safe!
      // console.log(action.payload.item); // COMPILE ERROR: Property 'item' does not exist!
      return state;

    case CartActionType.CLEAR_CART:
      // action is narrowed to: { type: CartActionType.CLEAR_CART }
      // console.log(action.payload); // COMPILE ERROR: Property 'payload' does not exist!
      return state;
  }
}
```

---

## Pros & Cons: Union vs. Enum

| Feature | Approach 1: Discriminated Union (Pure Strings) | Approach 2: Enum + Discriminated Union Hybrid |
| :--- | :--- | :--- |
| **Type Safety** | 🟢 **100% Perfect** | 🟢 **100% Perfect** |
| **Code Verbosity** | 🟢 **Low**. No extra runtime constructs to define, import, or manage. | 🔴 **Higher**. You must define both the Enum and the mapping union, and import both where needed. |
| **Autocomplete in IDE** | 🟢 **Excellent**. IDE prompts you with string literal suggestions. | 🟢 **Excellent**. Autocomplete via the Enum namespace (e.g., `CartActionType.`). |
| **Refactoring** | 🟢 **Excellent**. Renaming a type or type value propagates via IDE tools. | 🟢 **Excellent**. Renaming an Enum member propagates everywhere automatically. |
| **Bundle Size** | 🟢 **Zero overhead**. String literals disappear in JS compilation. | 🔴 **Small overhead**. Enums compile into real JavaScript objects (IIFEs), slightly increasing bundle size. |

---

## Summary Recommendation

The modern consensus in the React and TypeScript communities is **Approach 1: Discriminated Unions with string literals**. 

Using plain string literal unions is less verbose, compiles to smaller JavaScript code, and has superb support in modern editors. 

**Avoid using Enums without a Discriminated Union**, like this:
```typescript
// ❌ DO NOT DO THIS (Unsafe Enum payload)
enum ActionType { ADD_ITEM, REMOVE_ITEM }
interface Action {
  type: ActionType;
  payload: any; // 👈 Loses type-safety entirely!
}
```
If you decide to use Enums for organizational clarity, **always map each enum type to a specific payload** using a Discriminated Union as shown in **Approach 2**.
