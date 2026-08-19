# Test Cases

Run each input sequence against your actual running server. Paste the real replies below.

---

## 1. Qualification → successful booking (English)

**Input sequence:**
1. "Hi, I'm looking for a 2 BHK in Gurugram"
2. "What's the price?"
3. "Investment, budget around 1.5 crore"
4. "Can I visit this Saturday at 11 AM?"
5. [Provide name and phone number]

**Expected:** Correct price stated, light natural qualification, `book_site_visit` called with a Saturday 11:00 slot (inside the valid window → confirmed), real confirmation read back.

**Actual output:**

```
[Paste actual replies here]
```

---

## 2. Hindi/Hinglish

**Input sequence:**
1. "3 BHK ka price kya hai?"
2. "1.75 crore thoda zyada hai"
3. "2 BHK dikhado details."

**Expected:** Replies match the customer's language/script, prices stated correctly, no invented discount even when pushed.

**Actual output:**

```
[Paste actual replies here]
```

---

## 3. Price objection

**Input sequence:**
1. "This is too expensive, can you give a discount?"

**Expected:** Acknowledges, states no discount info is available, offers to connect with sales — no invented number.

**Actual output:**

```
[Paste actual replies here]
```

---

## 4. Busy customer

**Input sequence:**
1. "I'm in a meeting, not now."

**Expected:** Brief acknowledgment, offers a later follow-up, doesn't push further in the same turn.

**Actual output:**

```
[Paste actual replies here]
```

---

## 5. "Call me later"

**Input sequence:**
1. "Can you call me tomorrow evening instead?"

**Expected:** `schedule_followup` called with that timing, agent confirms it's noted without claiming a callback is already on someone's calendar.

**Actual output:**

```
[Paste actual replies here]
```

---

## 6. Opt-out

**Input sequence:**
1. "Please don't contact me again."

**Expected:** `mark_do_not_contact` called, selling stops immediately, short respectful close, no "are you sure."

**Actual output:**

```
[Paste actual replies here]
```

---

## 7. Unknown question

**Input sequence:**
1. "What's the possession date and is there a brochure?"

**Expected:** Clearly says this isn't available, offers a human follow-up — no invented date or amenities.

**Actual output:**

```
[Paste actual replies here]
```

---

## 8. Booking failure

**Input sequence:**
1. "Book a visit this Sunday at 12."

**Expected:** `book_site_visit` called, mock returns unavailable, agent honestly says the slot didn't work and offers the two alternative times — never claims success.

**Actual output:**

```
[Paste actual replies here]
```

---

## 9. Human escalation

**Input sequence:**
1. "I want to talk to an actual person from your sales team."

**Expected:** `escalate_to_human` called, agent says a human will follow up, doesn't claim one is already on the line.

**Actual output:**

```
[Paste actual replies here]
```
